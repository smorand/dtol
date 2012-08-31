# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#


def plugin11(what, caseSrc, caseDst):
	print "I'm plugin1.1 with %s from %s on %s" % (what, caseSrc, caseDst)

def plugin12(what, caseSrc, caseDst):
	from dtol.game.actions.generic import plugin2
	plugin2(what, caseSrc, caseDst)
