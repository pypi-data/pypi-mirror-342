"""OHCRN-LEI - LLM-based Extraction of Information
Copyright (C) 2025 Ontario Institute for Cancer Research

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
from typing import List

from ohcrn_lei.cli import die
from ohcrn_lei.extractHGNCSymbols import find_HGNC_symbols
from ohcrn_lei.llm_calls import call_gpt_api
from ohcrn_lei.pdf_to_text import convert_pdf_to_str_list
from ohcrn_lei.regex_utils import (
  get_chromosomes,
  get_coding_changes,
  get_genomic_changes,
  get_protein_changes,
  get_variant_ids,
)


class Task:
  """Task performs an extraction task. It gets configured with an
  LLM prompt and option al plugins.

  run() executes the task on a given input file.
  """

  prompt: str
  plugins: dict | None

  def __init__(self, prompt: str):
    """Constructor to create a new task with an LLM prompt.

    Args:
      prompt: LLM prmopt

    """
    self.prompt = prompt
    self.plugins = None

  def set_plugins(self, plugins: dict):
    """Sets the plugins for this task. Plugins are formatted
    as dicts with have the desired json key as keys and
    the desired operations as values.

    Args:
      plugins: a dictionary of plugins to add to the task

    """
    self.plugins = plugins

  # print string representation override
  def __str__(self):
    return "PROMPT:\n" + self.prompt + "\nPLUGINS:\n" + str(self.plugins)

  def run(self, inputfile: str, chunk_size=2, no_ocr=False, llm_mock=False) -> dict:
    """Run the task on the given input file. If the file has multiple
    pages use the chunk size to determine how many pages are processed
    in a single batch.

    Args:
      inputfile: Path to the input pdf or text file
      chunk_size: how many pages to process per batch
      no_ocr: disable OCR
      llm_mock: disable LLM call (for testing / debugging)

    Returns:
      A dictionary of the JSON output produced by LLM and plugins

    Raises:
      ValueError: If an invalid plugin was defined

    """
    if no_ocr:
      all_text = self.convert_txt_to_str_list(inputfile)
    else:
      print("Performing OCR")
      all_text = convert_pdf_to_str_list(inputfile)

    i = 0
    full_results = {}

    while i <= len(all_text) - (chunk_size - 1):
      print("Extracting from pages", i, "to", i + chunk_size - 1)
      pages_text = " ".join(all_text[i : i + chunk_size])

      # Prepare query
      query_msg = (
        "Use the given format to extract information from the following input: "
        + pages_text
      )
      print(" - Running LLM request")
      # Call the API to get JSON (dict) with the requested fields in the prompt
      llm_results = call_gpt_api(self.prompt, query_msg, "gpt-4o", llm_mock)
      # Add to llm dict
      page_key = "Pages " + str(i + 1) + "-" + str(i + chunk_size)
      full_results[page_key] = llm_results

      # Run plugins
      if self.plugins:
        print(" - Running plugins")
        for path, plugin_name in self.plugins.items():
          match plugin_name:
            case "trie_hgnc":
              pl_output = find_HGNC_symbols(pages_text)
              # remove duplicates and sort
              pl_output = sorted(set(pl_output))
            case "regex_hgvsg":
              pl_output = get_genomic_changes(pages_text)
            case "regex_hgvsc":
              pl_output = get_coding_changes(pages_text)
            case "regex_hgvsp":
              pl_output = get_protein_changes(pages_text)
            case "regex_variants":
              pl_output = get_variant_ids(pages_text)
            case "regex_chromosome":
              pl_output = get_chromosomes(pages_text)
            case _:
              # FIXME: This should probably be checked when the plugins are added, not when they're run.
              raise ValueError(f"Unrecognized plugin name: {plugin_name}")
          # full_results[page_key].update({path: pl_output})
          if path in full_results[page_key]:
            # if path already created by LLM output
            old_val = full_results[page_key][path]
            full_results[page_key][path] = self.integrateResults(old_val, pl_output)
          else:  # path doesn't exist yet, so we create it
            full_results[page_key][path] = pl_output

      i += chunk_size

    return full_results

  def integrateResults(self, xs, ys):
    """Intersects two lists (instead of sets)
    while preserving duplicates

    Args:
      xs: Any list
      ys: Any other list

    Returns:
      A list that is the (non-deduplicated) intersection of the inputs.

    """
    if type(xs) is not list:
      xs = [xs]
    if type(ys) is not list:
      ys = [ys]
    taken_js = set()
    for i in range(len(xs)):
      j = 0
      for j in range(len(ys)):
        if j not in taken_js and xs[i] == ys[j]:
          taken_js.add(j)
          break
    unused_js = set(j for j in range(len(ys))) - taken_js
    unused_ys = [ys[j] for j in unused_js]
    return xs + unused_ys

  def convert_txt_to_str_list(self, inputfile: str) -> List[str]:
    """Reads a text file and wraps it in a list.
    This simulates multi-page readout from a PDF

    Args:
      inputfile: Path to text file

    Returns:
      A mock list of pages (but really just the full text in a singleton list)

    """
    try:
      with open(inputfile, "r", encoding="utf-8") as instream:
        text = instream.read()
    except Exception as e:
      die(f"Unable to read file {inputfile}: {e}", os.EX_IOERR)
    # simulate multiple pages for plain text input
    return [text]
