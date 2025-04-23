#	pyradium - HTML presentation/slide show generator
#	Copyright (C) 2015-2023 Johannes Bauer
#
#	This file is part of pyradium.
#
#	pyradium is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pyradium is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pyradium; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import sys
import argparse
import pyradium
from .MultiCommand import MultiCommand
from .ActionRender import ActionRender
from .ActionShowStyleOpts import ActionShowStyleOpts
from .ActionModify import ActionModify
from .ActionServe import ActionServe
from .ActionAcroAdd import ActionAcroAdd
from .ActionAcroScan import ActionAcroScan
from .ActionAcroSort import ActionAcroSort
from .ActionAcroTex import ActionAcroTex
from .ActionPurge import ActionPurge
from .ActionHashPresentation import ActionHashPresentation
from .ActionDumpMetadata import ActionDumpMetadata
from .ActionSpellcheck import ActionSpellcheck
from .ActionDictAdd import ActionDictAdd
from .ActionTemplateHelper import ActionTemplateHelper
from .ActionStandalone import ActionStandalone
from .modify.BaseModifyCommand import BaseModifyCommand
from .standalone.BaseStandaloneCommand import BaseStandaloneCommand
from .Enums import PresentationFeature
from .GlobalConfig import GlobalConfig

def _geometry(text):
	text = text.split("x", maxsplit = 1)
	if len(text) != 2:
		raise argparse.ArgumentTypeError("Not a valid geometry: %s" % (text))
	return (int(text[0]), int(text[1]))

def _resource_dir(text):
	text = text.split(":", maxsplit = 1)
	if len(text) != 2:
		raise argparse.ArgumentTypeError("Not a valid resource directory/URI combination: %s" % (text))
	return (text[0], text[1])

def main():
	gc = GlobalConfig.read()
	mc = MultiCommand(description = "HTML presentation renderer", trailing_text = "version: pyradium v%s" % (pyradium.VERSION), run_method = True)

	def genparser(parser):
		parser.add_argument("--image-max-dimension", metavar = "pixels", type = int, default = 1920, help = "When rendering imaages, specifies the maximum dimension they're downsized to. The lower this value, the smaller the output files and the lower the quality. Defaults to %(default)d pixels.")
		parser.add_argument("-I", "--include-dir", metavar = "path", action = "append", default = [ ], help = "Specifies an additional include directory in which, for example, images are located which are referenced from the presentation. Can be issued multiple times.")
		parser.add_argument("-R", "--resource-dir", metavar = "path:uripath", type = _resource_dir, help = "Specifies the resource directory both as the actual deployment directory and the URI it has when serving the presentation. By default, the deployment directory of resources is identical to the output directory and the uripath is '.'.")
		parser.add_argument("--template-dir", metavar = "path", action = "append", default = [ ], help = "Specifies an additional template directories in which template style files are located. Can be issued multiple times.")
		parser.add_argument("-t", "--template-style", metavar = "name", default = "antonio", help = "Template style to use. Defaults to %(default)s.")
		parser.add_argument("-o", "--style-option", metavar = "key=value", action = "append", default = [ ], help = "Pass template-style specific options to the renderer. Must always be in the form of \"key=value\". Use the 'showstyleopts' command to find out which keys are supported for a given template.")
		parser.add_argument("-g", "--geometry", metavar = "width x height", type = _geometry, default = "1280x720", help = "Slide geometry, in pixels. Defaults to %(default)s.")
		parser.add_argument("-r", "--remove-pauses", action = "store_true", help = "Ignore all pause directives and just render the final slides.")
		parser.add_argument("--collapse-animation", action = "store_true", help = "Do not render animations as multiple slides, just show one complete slide.")
		parser.add_argument("-i", "--index-filename", metavar = "filename", default = "index.html", help = "Gives the name of the presentation index file. Defaults to %(default)s. Useful if you want to render multiple presentations in one subdirectory.")
		parser.add_argument("-j", "--inject-metadata", metavar = "filename", help = "Gives the option to inject variables into the presentation variable data. Must point to a JSON filename that contains a dictionary. Will take highest precedence. Useful for changing things like the presentation date on the command line.")
		parser.add_argument("-e", "--enable-presentation-feature", choices = [ enumitem.value for enumitem in PresentationFeature ], default = [ ], action = "append", help = "Enable a specific presentation feature. Can be one of %(choices)s and can be given multiple times.")
		parser.add_argument("-d", "--disable-presentation-feature", choices = [ enumitem.value for enumitem in PresentationFeature ], default = [ ], action = "append", help = "Disable a specific presentation feature. Can be one of %(choices)s and can be given multiple times.")
		parser.add_argument("-l", "--re-render-loop", action = "store_true", help = "Stay in a continuous loop, re-rendering the presentation if anything changes.")
		parser.add_argument("-D", "--deploy-presentation", action = "store_true", help = "Deploy presentation after rendering to a remote server using the mechanism indicated in the presentation metadata.")
		parser.add_argument("--deployment-name", metavar = "name", action = "append", default = [ ], help = "Deploy this deployment configuration. Can be specified multiple times to deploy on mutiple targets. Defaults to 'default'.")
		parser.add_argument("--re-render-watch", metavar = "path", action = "append", default = [ ], help = "By default, all include files and the template directory is being watched for changes. This option gives additional files or directories upon change of which the presentation should be re-rendered.")
		parser.add_argument("--trustworthy-source", action = "store_true", help = "By default, the presentation source code is considered not trustworthy and therefore primitives which allow remote code execution (like s:exec) are disabled by default. If you know that the source of your presentation is trustworthy and want to allow it to execute arbitrary code, then specify this parameter.")
		parser.add_argument("--allow-missing-svg-fonts", action = "store_true", help = "If a font is not present on the local system, pyradium aborts instead of rendering an SVG with replaced fonts. This option allows to render the presentation anyways.")
		parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite files in destination directory if they already exist.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be specified more than once.")
		parser.add_argument("infile", help = "Input XML file of the presentation.")
		parser.add_argument("outdir", help = "Output directory the presentation is put into.")
	mc.register("render", "Render a presentation", genparser, action = ActionRender)

	def genparser(parser):
		parser.add_argument("--template-dir", metavar = "path", action = "append", default = [ ], help = "Specifies an additional template directories in which template style files are located. Can be issued multiple times.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be specified more than once.")
		parser.add_argument("template_style", help = "Name of the template that should be shown.")
	mc.register("showstyleopts", "Show all options a specific template style supports", genparser, action = ActionShowStyleOpts)

	modify_commands = list(sorted(BaseModifyCommand.get_supported_cmd_list()))
	if len(modify_commands) > 0:
		def genparser(parser):
			parser.add_argument("subcommand", choices = modify_commands, help = "Name of subcommand to call.")
			parser.add_argument("params", nargs = argparse.REMAINDER, help = "Arguments for the respective sub-command.")
		mc.register("modify", "Modify a presentation through one of many sub-commands", genparser, action = ActionModify)

	def genparser(parser):
		parser.add_argument("-b", "--bind-addr", metavar = "addr", type = str, default = "127.0.0.1", help = "Address to bind to. Defaults to %(default)s.")
		parser.add_argument("-p", "--port", metavar = "port", type = int, default = 8123, help = "Port to serve directory under. Defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("dirname", help = "Directory that should be served.")
	mc.register("serve", "Serve a rendered presentation over HTTP", genparser, action = ActionServe)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("acrofile", help = "Acronym database JSON file.")
	mc.register("acroadd", "Add an acryonym to the acronym database", genparser, action = ActionAcroAdd, aliases = [ "aadd" ])

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("acrofile", help = "Acronym database JSON file.")
		parser.add_argument("infile", help = "Input XML file of the presentation.")
	mc.register("acroscan", "Scans a presentation and suggests acronyms that can be added", genparser, action = ActionAcroScan, aliases = [ "ascan" ])

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("acrofile", help = "Acronym database JSON file.")
	mc.register("acrosort", "Sort an acryonym database", genparser, action = ActionAcroSort, aliases = [ "asort" ])

	def genparser(parser):
		parser.add_argument("-i", "--itemsep", metavar = "distance", help = "Include an \\itemsep command inside the acronym directory.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite files if they already exist.")
		parser.add_argument("acrofile", help = "Acronym database JSON file.")
		parser.add_argument("tex_outfile", nargs = "?", default = "-", help = "TeX output file to generate. If omitted, defaults to stdout.")
	mc.register("acrotex", "Convert an acronym database to LaTeX format", genparser, action = ActionAcroTex)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
	mc.register("purge", "Purge the document cache", genparser, action = ActionPurge)

	def genparser(parser):
		parser.add_argument("-I", "--include-dir", metavar = "path", action = "append", default = [ ], help = "Specifies an additional include directory in which, for example, images are located which are referenced from the presentation. Can be issued multiple times.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("infile", help = "Input XML file of the presentation.")
	mc.register("hash", "Create a hash of a presentation and all dependencies to detect modifications", genparser, action = ActionHashPresentation)

	def genparser(parser):
		parser.add_argument("-p", "--pretty-print", action = "store_true", help = "Pretty print the output JSON data.")
		parser.add_argument("-I", "--include-dir", metavar = "path", action = "append", default = [ ], help = "Specifies an additional include directory in which, for example, images are located which are referenced from the presentation. Can be issued multiple times.")
		parser.add_argument("-j", "--inject-metadata", metavar = "filename", help = "Gives the option to inject variables into the presentation variable data. Must point to a JSON filename and will override the respective metadata fields of the presentation. Useful for changing things like the presentation date on the command line.")
		parser.add_argument("-o", "--outfile", metavar = "filename", default = "-", help = "Write JSON data to this file. May be '-' to write to stdout. Defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("infile", help = "Input XML file of the presentation.")
	mc.register("dumpmeta", "Dump the metadata dictionary in JSON format", genparser, action = ActionDumpMetadata)

	def genparser(parser):
		have_default_spellchecker = gc.has("spellcheck", "uri") or gc.has("spellcheck", "jar")
		group = parser.add_mutually_exclusive_group(required = not have_default_spellchecker)
		group.add_argument("-u", "--uri", metavar = "uri", default = gc.get("spellcheck", "uri"), help = "Connect to this running LanguageTool server URI.")
		group.add_argument("-j", "--jar", metavar = "jarfile", default = gc.get("spellcheck", "jar"), help = "Start a LanguageTool server using this languagetool-server.jar JAR, automatically connect to it and shut it down after use.")
		parser.add_argument("-l", "--language", metavar = "lang", default = "en-US", help = "Spellcheck in this language. Defaults to %(default)s.")
		parser.add_argument("-m", "--mode", choices = [ "print", "vim", "evim", "fulljson" ], default = gc.get("spellcheck", "mode") or "print", help = "Mode in which spellchecking is performed. Can be one of %(choices)s, defaults to %(default)s.")
		parser.add_argument("-o", "--outfile", metavar = "filename", help = "Write output to this file. By default, outputs to stdout.")
		parser.add_argument("--vim", action = "store_true", help = "Run vim to actually spellcheck the file in question.")
		parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite files if they already exist.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("infile", help = "Input XML file of the presentation.")
	mc.register("spellcheck", "Spellcheck an XML presentation file", genparser, action = ActionSpellcheck)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("infile", help = "Input file, needs to be a quickfix file in evim format.")
	mc.register("dictadd", "Add false-positive spellcheck errors to the dictionary", genparser, action = ActionDictAdd)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("template_name", help = "Name of the template to insert.")
	mc.register("template-helper", "Show different templates on stdout; used in conjunction with vim plugins", genparser, action = ActionTemplateHelper)

	standalone_commands = list(sorted(BaseStandaloneCommand.get_supported_cmd_list()))
	if len(standalone_commands) > 0:
		def genparser(parser):
			parser.add_argument("subcommand", choices = standalone_commands, help = "Name of subcommand to call.")
			parser.add_argument("params", nargs = argparse.REMAINDER, help = "Arguments for the respective sub-command.")
		mc.register("standalone", "Run one of various standalong tools through sub-commands", genparser, action = ActionStandalone)

	return mc.run(sys.argv[1:])

if __name__ == "__main__":
	sys.exit(main())
