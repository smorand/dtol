#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from django.core.management import execute_manager
import sys
import settings # Assumed to be in the same directory.
sys.path.insert(0, settings.APPLICATION_ROOT)
if type(settings.EXTERNAL_PATH) == list:
	sys.path.extend(settings.EXTERNAL_PATH)

if __name__ == "__main__":
	execute_manager(settings)

