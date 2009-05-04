#!/usr/bin/env python
#-*- coding:utf-8 -*-

#    Copyright 2009 Matthieu Gautier

#    This file is part of g-ed-it.
#
#    g-ed-it is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    g-ed-it is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with g-ed-it.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import gtk
import subprocess

import commitDialog

GLADE_FILE = os.path.join(os.path.dirname(__file__), "git_windows.glade")

class GitAction (object):
	def __init__(self,plugin):
		self.glade_xml = gtk.glade.XML(GLADE_FILE)
		self.commitDialog = commitDialog.CommitDialog(self.glade_xml,plugin)
		self.plugin = plugin
		pass
	
	def commit(self, button, window):
		fileUri = window.get_active_tab().get_document().get_uri_for_display()
		self.commitDialog.run(window,fileUri,True)
	
	def commit_current_file(self, button, window, commitTextMethod = None):
		fileUri = window.get_active_tab().get_document().get_uri_for_display()
		if commitTextMethod:
			text = commitTextMethod()
			if text != "":
				subprocess.call('git-commit -m "'+text+'" '+os.path.basename(fileUri),stdout=subprocess.PIPE,cwd=os.path.dirname(fileUri), shell=True)
				self.plugin.fast_update_ui()
			else:
				self.commitDialog.run(window,fileUri,False)
		else:
			self.commitDialog.run(window,fileUri,False)
	
	def add(self, button, window):
		fileUri = window.get_active_tab().get_document().get_uri_for_display()
		subprocess.call("git-add "+os.path.basename(fileUri),stdout=subprocess.PIPE,cwd=os.path.dirname(fileUri), shell=True)
		window.emit("active-tab-state-changed")
		pass
	
	def diff_head_index(self, button, window):
		fileUri = window.get_active_tab().get_document().get_uri_for_display()
		subprocess.call("git-diff --cached "+os.path.basename(fileUri),stdout=subprocess.PIPE,cwd=os.path.dirname(fileUri), shell=True)
		pass
	
	def diff_index_wt(self, button, window):
		fileUri = window.get_active_tab().get_document().get_uri_for_display()
		subprocess.call("git-diff "+os.path.basename(fileUri),stdout=subprocess.PIPE,cwd=os.path.dirname(fileUri), shell=True)
		pass
