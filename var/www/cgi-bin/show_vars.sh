#!/bin/bash
#############################################
# Show cgi variables and environment in bash
# 
# copyright (c) Charles Shapiro February 2018
#
# This file is part of raspi_blinky.
#   raspi_blinky is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   raspi_blinky is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with raspi_blinky.  If not, see <http://www.gnu.org/licenses/>.
#############################################

cat <<EOF
Content-Type: text/html

<html>
<head>
<title>Variables in CGI</title>
</head>
<body>
EOF
echo "<h1>Show CGI Environment</h1>"
echo "<h2>CGI Vars</h2>"
echo '<pre>'
cat - | tr '&' '\n'

echo '</pre>'

echo "<h2>Environment Vars</h2>"
echo '<pre>'

set | grep -v '^_'

echo '</pre>'

cat <<EOF
</body>
</html>
EOF
