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

from pyradium.xmlhooks.XMLHookRegistry import BaseHook, XMLHookRegistry, ReplacementFragment
from pyradium.Tools import XMLTools

@XMLHookRegistry.register_hook
class QRCodeHook(BaseHook):
	_TAG_NAME = "qrcode"

	@classmethod
	def handle(cls, rendered_presentation, node):
		# Text to render
		text = XMLTools.inner_text(node)

		# Render QR-code to SVG
		qrcode_renderer = rendered_presentation.renderer.get_custom_renderer("qrcode")
		qrcode_svg = qrcode_renderer.render({
			"data": text,
		})

		replacement_node = node.ownerDocument.createElement("s:img")
		replacement_node.setAttribute("value", qrcode_svg.data["svg"].decode())
		replacement_node.setAttribute("filetype", "svg")
		return ReplacementFragment(replacement = replacement_node)
