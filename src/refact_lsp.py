import os
import socket
import pathlib
from typing import Optional, Dict, Tuple
from .pylspclient.lsp_structs import *
from .pylspclient.lsp_endpoint import LspEndpoint
from .pylspclient.lsp_client import LspClient
from .pylspclient.json_rpc_endpoint import JsonRpcEndpoint

class LSP:
	def __init__(self, process, statusbar):
		self.statusbar = statusbar
		self.connect(process)

	def load_document(self, file_name: str, text: str, version: int = 1, languageId = LANGUAGE_IDENTIFIER.PYTHON):
		if languageId is None:
			languageId = LANGUAGE_IDENTIFIER.PYTHON

		uri = pathlib.Path(file_name).as_uri()
		try:
			self.lsp_client.didOpen(TextDocumentItem(uri, languageId, version, text=text))
		except:
			print("lsp didOpen error")

	def did_change(self, file_name: str, version: int, text: str, languageId = LANGUAGE_IDENTIFIER.PYTHON):
		if languageId is None:
			languageId = LANGUAGE_IDENTIFIER.PYTHON

		if file_name is None:
			return

		uri = pathlib.Path(file_name).as_uri()

		try:
			self.lsp_client.didChange(TextDocumentItem(uri, languageId, version, text=text), [TextDocumentContentChangeEvent(None, None, text)])
		except:
			print("lsp didChange error")

	def get_completions(self, file_name, pos: Tuple[int, int], multiline: bool = False):
		self.statusbar.update_statusbar("loading")
		params = {
			"max_new_tokens": 20,
			"temperature": 0.1
		}

		uri = pathlib.Path(file_name).as_uri()
		try:			
			res = self.lsp_endpoint.call_method(
				"refact/getCompletions",
				textDocument=TextDocumentIdentifier(uri),
				position=Position(pos[0], pos[1]),
				parameters=params,
				multiline=multiline)
			self.statusbar.update_statusbar("ok")
			return res
		except Exception as err:
			self.statusbar.update_statusbar("error", str(type(err)))

	def shutdown(self):
		try:
			self.lsp_client.shutdown()
		except:
			print("lsp error shutdown")

	def connect(self, process):
		capabilities = {}
		# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# s.connect(("127.0.0.1", 8002))
		# pipein, pipeout = s.makefile("wb", buffering=0), s.makefile("rb", buffering=0)

		# json_rpc_endpoint = JsonRpcEndpoint(pipein, pipeout)
		json_rpc_endpoint = JsonRpcEndpoint(process.stdin, process.stdout)
		self.lsp_endpoint = LspEndpoint(json_rpc_endpoint)
		self.lsp_client = LspClient(self.lsp_endpoint)
		try:
			self.lsp_client.initialize(process.pid, None, None, None, capabilities, "off", None)
		except Exception as err:
			self.statusbar.update_statusbar("error", str(type(err)))
			print("lsp initialize error")

def get_language_id(file_type):
	if file_type and not file_type.isspace():
		if file_type == "python":
			return LANGUAGE_IDENTIFIER.PYTHON
		elif file_type == "bibtex":
			return LANGUAGE_IDENTIFIER.BIBTEX
		elif file_type == "clojure":
			return LANGUAGE_IDENTIFIER.CLOJURE
		elif file_type == "coffeescript":
			return LANGUAGE_IDENTIFIER.COFFESCRIPT
		elif file_type == "c":
			return LANGUAGE_IDENTIFIER.C
		elif file_type == "cpp":
			return LANGUAGE_IDENTIFIER.CPP
		elif file_type == "csharp":
			return LANGUAGE_IDENTIFIER.CSHARP
		elif file_type == "css":
			return LANGUAGE_IDENTIFIER.CSS
		elif file_type == "diff":
			return LANGUAGE_IDENTIFIER.DIFF
		elif file_type == "dockerfile":
			return LANGUAGE_IDENTIFIER.DOCKERFILE
		elif file_type == "fsharp":
			return LANGUAGE_IDENTIFIER.FSHARP
		elif file_type == "go":
			return LANGUAGE_IDENTIFIER.GO
		elif file_type == "groovy":
			return LANGUAGE_IDENTIFIER.GROOVY
		elif file_type == "handlebars":
			return LANGUAGE_IDENTIFIER.HANDLEBARS
		elif file_type == "html":
			return LANGUAGE_IDENTIFIER.HTML
		elif file_type == "ini":
			return LANGUAGE_IDENTIFIER.INI
		elif file_type == "java":
			return LANGUAGE_IDENTIFIER.JAVA
		elif file_type == "javascript":
			return LANGUAGE_IDENTIFIER.JAVASCRIPT
		elif file_type == "json":
			return LANGUAGE_IDENTIFIER.JSON
		elif file_type == "latex":
			return LANGUAGE_IDENTIFIER.LATEX
		elif file_type == "less":
			return LANGUAGE_IDENTIFIER.LESS
		elif file_type == "lua":
			return LANGUAGE_IDENTIFIER.LUA
		elif file_type == "makefile":
			return LANGUAGE_IDENTIFIER.MAKEFILE
		elif file_type == "markdown":
			return LANGUAGE_IDENTIFIER.MARKDOWN
		elif file_type == "perl":
			return LANGUAGE_IDENTIFIER.Perl
		elif file_type == "php":
			return LANGUAGE_IDENTIFIER.PHP
		elif file_type == "powershell":
			return LANGUAGE_IDENTIFIER.POWERSHELL
		elif file_type == "jade":
			return LANGUAGE_IDENTIFIER.PUG
		elif file_type == "python":
			return LANGUAGE_IDENTIFIER.PYTHON
		elif file_type == "r":
			return LANGUAGE_IDENTIFIER.R
		elif file_type == "razor":
			return LANGUAGE_IDENTIFIER.RAZOR
		elif file_type == "ruby":
			return LANGUAGE_IDENTIFIER.RUBY
		elif file_type == "rust":
			return LANGUAGE_IDENTIFIER.RUST
		elif file_type == "sass":
			return LANGUAGE_IDENTIFIER.SASS
		elif file_type == "scss":
			return LANGUAGE_IDENTIFIER.SCSS
		elif file_type == "shaderlab":
			return LANGUAGE_IDENTIFIER.ShaderLab
		elif file_type == "shellscript":
			return LANGUAGE_IDENTIFIER.SHELL_SCRIPT
		elif file_type == "sql":
			return LANGUAGE_IDENTIFIER.SQL
		elif file_type == "swift":
			return LANGUAGE_IDENTIFIER.SWIFT
		elif file_type == "typescript":
			return LANGUAGE_IDENTIFIER.TYPE_SCRIPT
		elif file_type == "tex":
			return LANGUAGE_IDENTIFIER.TEX
		elif file_type == "vb":
			return LANGUAGE_IDENTIFIER.VB
		elif file_type == "xml":
			return LANGUAGE_IDENTIFIER.XML
		elif file_type == "xsl":
			return LANGUAGE_IDENTIFIER.XSL
		elif file_type == "yaml":
			return LANGUAGE_IDENTIFIER.YAML