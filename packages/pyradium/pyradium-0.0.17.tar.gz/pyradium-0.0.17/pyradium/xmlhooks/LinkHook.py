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

@XMLHookRegistry.register_hook
class LinkHook(BaseHook):
	_TAG_NAME = "link"

	@classmethod
	def handle(cls, rendered_presentation, node):
		href = node.getAttribute("href")
		replacement_node = node.ownerDocument.createElement("a")
		replacement_node.setAttribute("href", href)
		replacement_node.appendChild(node.ownerDocument.createTextNode(href))
		return ReplacementFragment(replacement = replacement_node, continue_descent = False)
