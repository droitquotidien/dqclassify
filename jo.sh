SOURCEDIR=$1
TARGETDIR=$2
if [ "X$SOURCEDIR" = "X" -o "X$TARGETDIR" = "X" ]
then
	echo "Usage: $0 sourcedir targetdir"
	exit 1
fi

gencsv () {
	echo "$1"
	dqclassify_csv $SOURCEDIR/jorf_$1.csv 1> $TARGETDIR/jorf_$1_mod_class.csv 2> $TARGETDIR/jorf_$1_mod_class.log
	dqclassify_test_csv $TARGETDIR/jorf_$1_mod_class.csv 7
}
#gencsv 2023
#gencsv 2022
gencsv 2021
gencsv 2020
gencsv 2019
gencsv 2018
gencsv 2017
gencsv 2016
gencsv 2015
gencsv 2014
gencsv 2013
gencsv 2012
gencsv 2011
gencsv 2010
gencsv 2009
gencsv 2008
gencsv 2007
gencsv 2006
gencsv 2005
gencsv 2004
gencsv 2003
gencsv 2002
gencsv 2001
gencsv 2000
gencsv 1999
gencsv 1998
gencsv 1997
gencsv 1996
gencsv 1995
gencsv 1994
gencsv 1993
gencsv 1992
gencsv 1991
gencsv 1990

