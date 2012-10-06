#!/usr/bin/env php
<?

error_reporting(E_ALL ^ E_NOTICE);

$confDir = '/home/sebastien/documents/Loisirs/Dungeon Twister/dtonline/config/boards';

$dir = opendir($confDir);

while (($entry = readdir($dir))) {
	if ($entry == "." || $entry == "..") continue;
	$file = $confDir . "/" . $entry;
	require $file;
	$f = fopen('csv/' . str_replace('.conf.php', '', $entry) . '.csv', 'w');
        if (substr($entry, 0, 6) == 'dalles') {
            foreach($dalles as $dalleNum => $board) {
                foreach ($board as $case => $def) {
                        fwrite($f, strtolower(str_replace(array('FLOOR_MODIFIER_', 'FLOOR_', 'WALL_'), '', "$dalleNum;$case;{$board[$case]['sol']};{$board[$case]['sol_modifier']};{$board[$case]['mur_nord']};{$board[$case]['mur_est']};{$board[$case]['mur_sud']};{$board[$case]['mur_ouest']}\n")));
                }
            }
        } else {
            foreach ($board as $case => $def) {
                fwrite($f, strtolower(str_replace(array('FLOOR_MODIFIER_', 'FLOOR_', 'WALL_'), '', "$case;{$board[$case]['sol']};{$board[$case]['sol_modifier']};{$board[$case]['mur_nord']};{$board[$case]['mur_est']};{$board[$case]['mur_sud']};{$board[$case]['mur_ouest']}\n")));
            }
        }
	fclose($f);
}
