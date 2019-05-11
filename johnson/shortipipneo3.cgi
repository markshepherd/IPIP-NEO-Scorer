#!/usr/local/bin/perl

use CGI;

MAIN:
{
# Read in identifying information
  $query = new CGI;

# Extract identifying variables
  $Sex = $query->param('Sex');
  $Age = $query->param('Age');
  $Nick = $query->param('Nick');
  $Country = $query->param('Country');

# Get the item responses
  for ($i = 1; $i < 121; $i++) {
  $item = "Q$i";
  $Q[$i] = $query->param($item);
}

#Create lines of item responses
for ($i = 0; $i < 60; $i++) {
  $line1[$i] = $Q[$i + 1];
  $line2[$i] = $Q[$i + 61];
}

# Create gender variable

  if ($Sex eq "Male") {
$Gender = 1;
}
  if ($Sex eq "Female") {
$Gender = 2;
}

#Get time
$t = time();
($sec,$min,$hour,$dom,$mon,$year,$wday,$yday,$isdst) = localtime($t);

# Update data file
$datafile = "sipipitem.dat";
open (ITEM_FILE, ">>$datafile") || die("Cannot open data file.");
flock (ITEM_FILE, 2);
printf ITEM_FILE ("%1d%2d%2d%2d%2d%2d%2d%3d %s %s", $Gender,$Age,$sec,$min,$hour,$dom,$mon,$year,$Nick,$Country);
printf ITEM_FILE ("\n");
foreach $line1 (@line1) {
  printf ITEM_FILE ("%1d", $line1);
}
printf ITEM_FILE ("\n");
foreach $line2 (@line2) {
  printf ITEM_FILE ("%1d", $line2);
}
printf ITEM_FILE ("\n");
flock (ITEM_FILE, 8);
close(ITEM_FILE);

# New error checking routines
# Count missing values
  $zeroes = 0;
  for ($i = 1; $i < 121; $i++) { 
    if ($Q[$i] == 0){
    ($zeroes += 1);
}
}
#If number of zeroes > 10, halt execution, otherwise, replace missing values with 3 and warn
  if ($zeroes > 10){
  print $query->header;
  print $query->start_html(-title=>'Too Many Missing Answers');
  print "You skipped too many items to allow the production of meaningful results. To receive feedback you must respond to some of the items you skipped. No more than 10 items can be omitted for this inventory to be scored.";
  exit;
}
  if ($zeroes > 0){
$warning = "Warning: The number of skipped items is $zeroes. Missing items were scored as if the middle option were chosen. Results are most accurate when no items are skipped.";
  for ($i = 1; $i < 121; $i++) { 
    if ($Q[$i] == 0){
    ($Q[$i] = 3);
}
}
}
# P array unreverse-scores the reverse-keyed items
  for ($i = 1; $i < 121; $i++) { 
    $P[$i] = $Q[$i];
}
$P[9]=6-$P[9];
$P[19]=6-$P[19];
$P[24]=6-$P[24];
$P[30]=6-$P[30];
$P[39]=6-$P[39];
$P[40]=6-$P[40];
$P[48]=6-$P[48];
$P[49]=6-$P[49];
$P[51]=6-$P[51];
$P[53]=6-$P[53];
$P[54]=6-$P[54];
$P[60]=6-$P[60];
$P[62]=6-$P[62];
$P[67]=6-$P[67];
$P[68]=6-$P[68];
$P[69]=6-$P[69];
$P[70]=6-$P[70];
$P[73]=6-$P[73];
$P[74]=6-$P[74];
$P[75]=6-$P[75];
$P[78]=6-$P[78];
$P[79]=6-$P[79];
$P[80]=6-$P[80];
$P[81]=6-$P[81];
$P[83]=6-$P[83];
$P[84]=6-$P[84];
$P[85]=6-$P[85];
$P[88]=6-$P[88];
$P[89]=6-$P[89];
$P[90]=6-$P[90];
$P[92]=6-$P[92];
$P[94]=6-$P[94];
$P[96]=6-$P[96];
$P[97]=6-$P[97];
$P[98]=6-$P[98];
$P[99]=6-$P[99];
$P[100]=6-$P[100];
$P[101]=6-$P[101];
$P[102]=6-$P[102];
$P[103]=6-$P[103];
$P[104]=6-$P[104];
$P[105]=6-$P[105];
$P[106]=6-$P[106];
$P[107]=6-$P[107];
$P[108]=6-$P[108];
$P[109]=6-$P[109];
$P[110]=6-$P[110];
$P[111]=6-$P[111];
$P[113]=6-$P[113];
$P[114]=6-$P[114];
$P[115]=6-$P[115];
$P[116]=6-$P[116];
$P[118]=6-$P[118];
$P[119]=6-$P[119];
$P[120]=6-$P[120];
# Count longest strings of each response category. $tlong is the longest string found so far. $llong is the longest string in the inventory.
  for ($i = 1; $i < 6; $i++) {
  $llong[$i] = 1;
  $tlong[$i] = 1;
}  

for ($i = 2; $i < 121; $i++) { 
  $j = ($i - 1);
  $k = $P[$i];
  if ($P[$i] == $P[$j]) {
  $tlong[$k] += 1;
}
  if ($tlong[$k] > $llong[$k]){
  $llong[$k] = $tlong[$k];
}
  if ($P[$i] != $P[$j]){
  $tlong[$k] = 1;
}
}
#If too many consecutive identical responses, halt
  if ($llong[1] > 9){
  print $query->header;
  print $query->start_html(-title=>'Too Many Consecutive Identical Answers');
  print "You used the Very Inaccurate response option $llong[1] times in a row. This suggests that you are choosing a response without considering the content of the item. Because the results would be meaningless, this program will end.";
  exit;
}
#If too many consecutive identical responses, halt
  if ($llong[2] > 9){
  print $query->header;
  print $query->start_html(-title=>'Too Many Consecutive Identical Answers');
  print "You used the Moderately Inaccurate response option $llong[2] times in a row. This suggests that you are choosing a response without considering the content of the item. Because the results would be meaningless, this program will end.";
  exit;
}
#If too many consecutive identical responses, halt
  if ($llong[3] > 8){
  print $query->header;
  print $query->start_html(-title=>'Too Many Consecutive Identical Answers');
  print "You used the Neither Accurate Nor Inaccurate response option $llong[3] times in a row. This suggests that you are choosing a response without considering the content of the item. Because the results would be meaningless, this program will end.";
  exit;
}
#If too many consecutive identical responses, halt
  if ($llong[4] > 11){
  print $query->header;
  print $query->start_html(-title=>'Too Many Consecutive Identical Answers');
  print "You used the Moderately Accurate response option $llong[4] times in a row. This suggests that you are choosing a response without considering the content of the item. Because the results would be meaningless, this program will end.";
  exit;
}
#If too many consecutive identical responses, halt
  if ($llong[5] > 9){
  print $query->header;
  print $query->start_html(-title=>'Too Many Consecutive Identical Answers');
  print "You used the Very Accurate response option $llong[5] times in a row. This suggests that you are choosing a response without considering the content of the item. Because the results would be meaningless, this program will end.";
  exit;
}
# Score facet scales
  for ($i = 1; $i < 31; $i++) {
    $k = 0;
    for ($j = 0; $j < 4; $j++) { 
    ($ss[$i] += $Q[$i+$k]);
    ($k += 30);
}
}

# Number each facet set from 1-6

  ($j = 0);
  for ($i = 1; $i < 7; $i++) {
  ($NF[$i] = $ss[$i + $j]);
  ($EF[$i] = $ss[$i + $j + 1]);
  ($OF[$i] = $ss[$i + $j + 2]);
  ($AF[$i] = $ss[$i + $j + 3]);
  ($CF[$i] = $ss[$i + $j + 4]);
  ($j += 4);
}

# Score domain scales  
#          1         2          3         4         5         6
  ($N = $ss[1] + $ss[6]  + $ss[11] + $ss[16] + $ss[21] + $ss[26]);
  ($E = $ss[2] + $ss[7]  + $ss[12] + $ss[17] + $ss[22] + $ss[27]);
  ($O = $ss[3] + $ss[8]  + $ss[13] + $ss[18] + $ss[23] + $ss[28]);
  ($A = $ss[4] + $ss[9]  + $ss[14] + $ss[19] + $ss[24] + $ss[29]);
  ($C = $ss[5] + $ss[10] + $ss[15] + $ss[20] + $ss[25] + $ss[30]);

# Standardize scores

  if ($Sex eq "Male" && $Age < 21) {
@norm = (0,67.84,80.70,85.98,81.98,79.66,15.83,15.37,12.37,14.66,14.49,
  11.72,11.93,10.58,12.38,11.67,9.63,3.76,4.41,4.25,3.83,3.25,3.38,
  13.76,12.23,14.06,11.54,14.67,14.41,3.78,4.17,3.66,3.15,3.38,3.68,
  16.68,14.51,14.52,12.84,15.47,11.86,2.96,3.87,3.31,3.16,3.50,3.17,
  13.18,14.85,15.37,12.73,12.01,13.96,3.69,3.44,3.10,4.05,3.94,3.35,
  15.31,10.97,15.22,13.61,12.35,12.08,2.55,3.93,2.92,3.65,3.24,4.02);
  ($id = "males less than 21 years of age");
}

  if ($Sex eq "Male" && $Age > 20 && $Age < 41) {
@norm = (0,66.97,78.90,86.51,84.22,85.50,16.48,15.21,12.65,13.10,14.27,
  11.44,11.75,10.37,12.11,12.18,9.13,3.76,4.30,4.12,3.81,3.52,3.48,
  13.31,11.34,14.58,12.07,13.34,14.30,3.80,3.99,3.58,3.23,3.43,3.53,
  15.94,14.94,14.60,13.14,16.11,11.66,3.18,3.63,3.19,3.39,3.25,3.72,
  12.81,15.93,15.37,14.58,11.43,13.77,3.69,3.18,2.92,3.70,3.57,3.29,
  15.80,12.05,15.68,15.36,13.27,13.31,2.44,4.26,2.76,3.39,3.31,4.03);
  ($id = "men between 21 and 40 years of age");
}
  if ($Sex eq "Male" && $Age > 40 && $Age < 61) {
@norm = (0,64.11,77.06,83.04,88.33,91.27,16.04,14.31,13.05,11.76,13.35,
  10.79,11.60,9.78,11.85,11.24,8.81,3.56,4.16,3.94,3.62,3.55,3.35,
  13.22,10.45,14.95,12.27,11.82,14.32,3.71,3.68,3.44,3.30,3.23,3.29,
  14.65,14.66,14.76,12.69,15.40,11.04,3.35,3.59,3.02,3.44,3.43,3.93,
  13.42,16.94,15.65,15.66,11.96,14.21,3.49,2.83,2.88,3.33,3.34,3.17,
  16.19,13.33,16.56,16.51,14.05,14.60,2.25,4.32,2.50,2.93,3.13,3.78);
  ($id = "men between 41 and 60 years of age");
}

  if ($Sex eq "Male" && $Age > 60) {
@norm = (0,58.42,79.73,79.78,90.20,95.31,15.48,13.63,12.21,11.73,11.99,
  9.81,11.46,8.18,11.08,9.91,8.24,3.54,4.31,3.59,3.82,3.36,3.28,
  14.55,11.19,15.29,12.81,11.03,15.02,3.47,3.58,3.10,3.25,2.88,3.16,
  14.06,14.22,14.34,12.42,14.61,10.11,3.13,3.64,2.90,3.20,3.89,4.02,
  13.96,17.74,15.76,16.18,11.87,14.00,3.13,2.39,2.74,3.41,3.50,3.11,
  16.32,14.41,17.54,16.65,14.98,15.18,2.31,4.49,2.30,2.68,2.76,3.61);
  ($id = "men over 60 years of age");
}

  if ($Sex eq "Female" && $Age < 21) {
@norm = (0,73.41,84.26,89.01,89.14,81.27,15.61,14.98,11.84,13.21,14.38,
  13.31,13.09,11.05,12.11,12.48,11.30,3.62,4.18,4.20,3.82,3.30,3.47,
  14.47,13.12,14.03,12.67,14.69,15.34,3.60,4.13,3.68,3.09,3.48,3.42,
  16.86,15.93,16.02,12.95,15.06,12.17,2.89,3.44,2.95,3.24,3.51,3.02,
  13.46,16.11,16.66,13.73,13.23,15.70,3.72,2.94,2.69,4.14,3.79,2.84,
  15.30,11.11,15.62,14.69,12.73,11.82,2.54,4.17,2.76,3.37,3.19,4.01
);
  ($id = "females less than 21 years of age");
}

   if ($Sex eq "Female" && $Age > 20 && $Age < 41) {
@norm = (0,72.14,80.78,88.25,91.91,87.57,16.16,14.64,12.15,11.39,13.87,
  13.08,12.72,10.79,12.20,12.71,10.69,3.68,4.13,4.07,3.79,3.58,3.64,
  14.05,11.92,14.25,12.77,12.84,14.96,3.66,4.05,3.61,3.24,3.53,3.31,
  15.64,15.97,16.41,12.84,15.28,12.06,3.34,3.30,2.69,3.44,3.47,3.46,
  13.15,17.34,16.81,15.57,12.98,15.52,3.71,2.61,2.53,3.50,3.57,2.87,
  16.02,12.67,16.36,16.11,13.56,12.91,2.34,4.51,2.54,3.05,3.23,4.18
);
  ($id = "women between 21 and 40 years of age");
}
  if ($Sex eq "Female" && $Age > 40 && $Age < 61) {
@norm = (0,67.38,78.62,86.15,95.73,93.45,16.10,14.19,12.62,9.84,12.94,
  12.05,11.19,10.07,12.07,11.98,10.07,3.72,4.03,3.97,3.73,3.69,3.56,
  14.10,10.84,14.51,13.03,11.08,15.00,3.72,3.86,3.50,3.46,3.42,3.26,
  14.43,16.00,16.37,12.58,14.87,11.85,3.49,3.20,2.58,3.45,3.65,3.74,
  13.79,18.16,17.04,17.02,13.41,15.82,3.52,2.21,2.40,2.88,3.30,2.71,
  16.50,13.68,17.29,17.16,14.35,14.41,2.16,4.51,2.27,2.73,3.13,3.86);
  ($id = "women between 41 and 60 years of age");
}

  if ($Sex eq "Female" && $Age > 60) {
@norm = (0,63.48,78.22,81.56,97.17,96.44,14.92,12.73,12.66,9.52,12.43,
  11.39,10.52,9.10,12.00,10.21,9.87,3.61,3.82,3.68,3.61,3.58,3.44,
  14.85,10.93,14.19,12.76,10.08,15.65,3.43,3.70,3.64,3.26,3.20,3.04,
  13.15,15.95,15.73,11.80,14.21,10.81,3.71,3.12,2.74,3.26,3.47,3.89,
  14.19,18.64,17.13,17.98,13.58,15.83,3.39,1.90,2.18,2.56,3.38,2.85,
  16.50,15.15,18.34,17.19,14.70,15.11,2.24,4.07,1.81,2.49,3.15,3.66);
  ($id = "women over 60 years of age");
}

  ($SN =  (10 * ($N - $norm[1])/$norm[6]) + 50);
  ($SE =  (10 * ($E - $norm[2])/$norm[7]) + 50);
  ($SO =  (10 * ($O - $norm[3])/$norm[8]) + 50);
  ($SA =  (10 * ($A - $norm[4])/$norm[9]) + 50);
  ($SC =  (10 * ($C - $norm[5])/$norm[10]) + 50);

  for ($i = 1; $i < 7; $i++) {
    ($SNF[$i] = 50 + (10 * ($NF[$i]-$norm[$i + 10])/$norm[$i + 16]));
    ($SEF[$i] = 50 + (10 * ($EF[$i]-$norm[$i + 22])/$norm[$i + 28]));
    ($SOF[$i] = 50 + (10 * ($OF[$i]-$norm[$i + 34])/$norm[$i + 40]));
    ($SAF[$i] = 50 + (10 * ($AF[$i]-$norm[$i + 46])/$norm[$i + 52]));
    ($SCF[$i] = 50 + (10 * ($CF[$i]-$norm[$i + 58])/$norm[$i + 64]));
}


# Cubic approximations for percentiles

  ($SNP = int(210.335958661391 - (16.7379362643389 * $SN) + (0.405936512733332 * $SN ** 2) - (0.00270624341822222 * $SN ** 3)));
  ($SEP = int(210.335958661391 - (16.7379362643389 * $SE) + (0.405936512733332 * $SE ** 2) - (0.00270624341822222 * $SE ** 3)));
  ($SOP = int(210.335958661391 - (16.7379362643389 * $SO) + (0.405936512733332 * $SO ** 2) - (0.00270624341822222 * $SO ** 3)));
  ($SAP = int(210.335958661391 - (16.7379362643389 * $SA) + (0.405936512733332 * $SA ** 2) - (0.00270624341822222 * $SA ** 3)));
  ($SCP = int(210.335958661391 - (16.7379362643389 * $SC) + (0.405936512733332 * $SC ** 2) - (0.00270624341822222 * $SC ** 3)));

  if ($SN < 27) {$SNP = 1};
  if ($SE < 27) {$SEP = 1};
  if ($SO < 27) {$SOP = 1};
  if ($SA < 27) {$SAP = 1};
  if ($SC < 27) {$SCP = 1};

  if ($SN > 73) {$SNP = 99};
  if ($SE > 73) {$SEP = 99};
  if ($SO > 73) {$SOP = 99};
  if ($SA > 73) {$SAP = 99};
  if ($SC > 73) {$SCP = 99};

# Create percentile scores and low, average, high labels for facets

  for ($i = 1; $i < 7; $i++) {
    $fflev[$i] = $SNF[$i];
    if ($SNF[$i] < 45) {
      ($flev[$i] = "low"); 
}
    if ($SNF[$i] >= 45 && $SNF[$i] <= 55) {
      ($flev[$i] = "average");
}
    if ($SNF[$i] > 55) {
      ($flev[$i] = "high");
}
  ($SNFP[$i] = int(210.335958661391 - (16.7379362643389 * $SNF[$i]) + (0.405936512733332 * $SNF[$i] ** 2) - (0.00270624341822222 * $SNF[$i] ** 3)));
  if ($SNF[$i] < 27) {$SNFP[$i] = 1};
  if ($SNF[$i] > 73) {$SNFP[$i] = 99};
}
  for ($i = 1; $i < 7; $i++) {
    $fflev[$i + 6] = $SEF[$i];
    if ($SEF[$i] < 45) {
      ($flev[$i + 6] = "low");
}
    if ($SEF[$i] >= 45 && $SEF[$i] <= 55) {
      ($flev[$i + 6] = "average");
}
    if ($SEF[$i] > 55) {
      ($flev[$i + 6] = "high");
}
  ($SEFP[$i] = int(210.335958661391 - (16.7379362643389 * $SEF[$i]) + (0.405936512733332 * $SEF[$i] ** 2) - (0.00270624341822222 * $SEF[$i] ** 3)));
  if ($SEF[$i] < 27) {$SEFP[$i] = 1};
  if ($SEF[$i] > 73) {$SEFP[$i] = 99};
}

  for ($i = 1; $i < 7; $i++) {
    $fflev[$i + 12] = $SOF[$i];
    if ($SOF[$i] < 45) {
      ($flev[$i + 12] = "low");
}
    if ($SOF[$i] >= 45 && $SOF[$i] <= 55) {
      ($flev[$i + 12] = "average");
}
    if ($SOF[$i] > 55) {
      ($flev[$i + 12] = "high");
}
  ($SOFP[$i] = int(210.335958661391 - (16.7379362643389 * $SOF[$i]) + (0.405936512733332 * $SOF[$i] ** 2) - (0.00270624341822222 * $SOF[$i] ** 3)));
  if ($SOF[$i] < 27) {$SOFP[$i] = 1};
  if ($SOF[$i] > 73) {$SOFP[$i] = 99};
}

  for ($i = 1; $i < 7; $i++) {
    $fflev[$i + 18] = $SAF[$i];
    if ($SAF[$i] < 45) {
      ($flev[$i + 18] = "low");
}
    if ($SAF[$i] >= 45 && $SAF[$i] <= 55) {
      ($flev[$i + 18] = "average");
}
    if ($SAF[$i] > 55) {
      ($flev[$i + 18] = "high");
}
  ($SAFP[$i] = int(210.335958661391 - (16.7379362643389 * $SAF[$i]) + (0.405936512733332 * $SAF[$i] ** 2) - (0.00270624341822222 * $SAF[$i] ** 3)));
  if ($SAF[$i] < 27) {$SAFP[$i] = 1};
  if ($SAF[$i] > 73) {$SAFP[$i] = 99};
}

  for ($i = 1; $i < 7; $i++) {
    $fflev[$i + 24] = $SCF[$i];
    if ($SCF[$i] < 45) {
      ($flev[$i + 24] = "low");
}
    if ($SCF[$i] >= 45 && $SCF[$i] <= 55) {
      ($flev[$i + 24] = "average");
}
    if ($SCF[$i] > 55) {
      ($flev[$i + 24] = "high");
}
  ($SCFP[$i] = int(210.335958661391 - (16.7379362643389 * $SCF[$i]) + (0.405936512733332 * $SCF[$i] ** 2) - (0.00270624341822222 * $SCF[$i] ** 3)));
  if ($SCF[$i] < 27) {$SCFP[$i] = 1};
  if ($SCF[$i] > 73) {$SCFP[$i] = 99};
}

#Create graphs

  ($WEP = 4.1 * $SEP);
 for ($i = 0; $i < 7; $i++) {
    ($WE[$i] = (4.1 * $SEFP[$i]));
}

  ($WAP = 4.1 * $SAP);
 for ($i = 0; $i < 7; $i++) {
    ($WA[$i] = (4.1 * $SAFP[$i]));
}
 
  ($WCP = 4.1 * $SCP);
 for ($i = 0; $i < 7; $i++) {
    ($WC[$i] = (4.1 * $SCFP[$i]));
}

  ($WNP = 4.1 * $SNP);
 for ($i = 0; $i < 7; $i++) {
    ($WN[$i] = (4.1 * $SNFP[$i]));
}

  ($WOP = 4.1 * $SOP);
 for ($i = 0; $i < 7; $i++) {
    ($WO[$i] = (4.1 * $SOFP[$i]));
}

  print $query->header;
  print $query->start_html(-title=>'IPIP-NEO Report for $Nick');
  print <<ENDOFTEXT;
<H1>IPIP-NEO Report for $Nick</h1>
<basefont = 3>
<font = +1><B>NOTE: The report sent to your computer screen upon the completion of the IPIP-NEO is only a temporary web page. When you exit your web browser you will not be able to return to this URL to re-access your report. No copies of the report are sent to anyone. IF YOU WANT A PERMANENT COPY OF THE REPORT, YOU MUST SAVE THE WEB PAGE TO YOUR HARD DRIVE OR OTHER STORAGE MEDIUM, AND/OR PRINT THE REPORT WHILE YOU ARE STILL VIEWING IT IN YOUR WEB BROWSER. Probably the best way to save the report is to select and copy the entire page (Ctrl-A, Ctrl-C on most browsers), paste it into a word processor, and save the document. </b></font><p><p> 

This report compares $Nick from the country $Country to other $id. (The name used in this report is either a nickname chosen by the person taking the test, or, if a valid nickname was not chosen, a random nickname generated by the program.)<P><p>

This report estimates the individual's level on each of the five broad  personality domains of the Five-Factor Model. The description of each one of the five broad domains is followed by a more detailed description of personality according to the six subdomains that comprise each domain.<p><p>

<I>A note on terminology</i>. Personality traits describe, relative to other people, the frequency or intensity of a person's feelings, thoughts, or behaviors. Possession of a trait is therefore a matter of degree. We might describe two individuals as <I>extraverts</i>, but still see one as more extraverted than the other. This report uses expressions such as "extravert" or "high in extraversion" to describe someone who is likely to be seen by others as relatively extraverted. The computer program that generates this report classifies you as low, average, or high in a trait according to whether your score is approximately in the lowest 30%, middle 40%, or highest 30% of scores obtained by people of your sex and roughly your age. Your numerical scores are reported and graphed as <I>percentile estimates</i>. For example, a score of "60" means that your level on that trait is estimated to be higher than 60% of persons of your sex and age.<p><p>

Please keep in mind that "low," "average," and "high" scores on a personality test are neither absolutely good nor bad. A particular level on any trait will probably be neutral or irrelevant for a great many activites, be helpful for accomplishing some things, and detrimental for accomplishing other things.

As with any personality inventory, scores and descriptions can only approximate an individual's actual personality. High and low score descriptions are usually accurate, but average scores close to the low or high boundaries might misclassify you as only average. On each set of six subdomain scales it is somewhat uncommon but certainly possible to score high in some of the subdomains and low in the others. In such cases more attention should be paid to the subdomain scores than to the broad domain score. Questions about the accuracy of your results are best resolved by showing your report to people who know you well.<p><p>

John A. Johnson wrote descriptions of the five domains and thirty subdomains. These descriptions are based on an extensive reading of the scientific literature on personality measurement. Although Dr. Johnson would like to be acknowledged as the author of these materials if they are reproduced, he has placed them in the public domain.<p><p>
ENDOFTEXT

  print $warning;
  
#Report based on low, average, or high scores
#Report based on low, average, or high scores

  ($LO = 45);
  ($HI = 55);

  print <<ENDOFTEXT;

<H2>Extraversion</h2>

Extraversion is marked by pronounced engagement with the external world. Extraverts enjoy being with people, are full of energy, and often experience
positive emotions. They tend to be enthusiastic, action-oriented, individuals who are likely to say "Yes!" or "Let's go!" to opportunities for excitement.
In groups they like to talk, assert themselves, and draw attention to
themselves.<p><p>

Introverts lack the exuberance, energy, and activity levels of extraverts. They tend to be quiet, low-key, deliberate, and disengaged from the social world. Their lack of social involvement should <U>not</u> be interpreted as shyness or depression; the introvert simply needs less stimulation than an extravert and prefers to be alone. The independence and reserve of the introvert is sometimes mistaken as unfriendliness or arrogance. In reality, an introvert who scores high on the agreeableness dimension will not seek others out but will be quite pleasant when approached.<p><p>

<table>
<tr><td>DOMAIN/Facet</td><td>Score</td><td><img src='grphhead.jpg'></td></tr>
<tr><td>EXTRAVERSION</td><td>$SEP</td><td><img src='bargray.jpg' width=$WEP height='20'></td></tr>
<tr><td>..Friendliness</td><td>$SEFP[1]</td><td><img src='bargray.jpg' width=$WE[1] height='20'></td></tr>
<tr><td>..Gregariousness</td><td>$SEFP[2]</td><td><img src='bargray.jpg' width=$WE[2] height='20'></td></tr>
<tr><td>..Assertiveness</td><td>$SEFP[3]</td><td><img src='bargray.jpg' width=$WE[3] height='20'></td></tr>
<tr><td>..Activity Level</td><td>$SEFP[4]</td><td><img src='bargray.jpg' width=$WE[4] height='20'></td></tr>
<tr><td>..Excitement-Seeking</td><td>$SEFP[5]</td><td><img src='bargray.jpg' width=$WE[5] height='20'></td></tr>
<tr><td>..Cheerfulness</td><td>$SEFP[6]</td><td><img src='bargray.jpg' width=$WE[6] height='20'></td></tr>
</table>

ENDOFTEXT

  if ($SE < $LO) {
      print <<ENDOFTEXT;

Your score on Extraversion is low, indicating you are introverted, reserved, and quiet. You enjoy solitude and solitary activities. Your socializing tends to be restricted to a few close friends.<P><P>
ENDOFTEXT
}

  if ($SE >= $LO && $SE <= $HI) {
      print <<ENDOFTEXT;
Your score on Extraversion is average, indicating you are neither a subdued loner nor a jovial chatterbox. You enjoy time with others but also time alone.<P><P>
ENDOFTEXT
}


  if ($SE > $HI) {
      print <<ENDOFTEXT;
Your score on Extraversion is high, indicating you are sociable, outgoing, energetic, and lively. You prefer to be around people much of the time.<P><P>
ENDOFTEXT
}

  print <<ENDOFTEXT;

<H3>Extraversion Facets</h3>

<ul>
<li> <I>Friendliness</i>. Friendly people genuinely like other people and openly
     demonstrate positive feelings toward others. They make friends quickly
     and it is easy for them to form close, intimate relationships. Low scorers
     on Friendliness are not necessarily cold and hostile, but they do not reach
     out to others and are perceived as distant and reserved. Your level of
     friendliness is $flev[7].</li>
<li> <I>Gregariousness</i>. Gregarious people find the company of others
     pleasantly stimulating and rewarding. They enjoy the excitement of
     crowds. Low scorers tend to feel overwhelmed by, and therefore actively
     avoid, large crowds. They do not necessarily dislike being with people
     sometimes, but their need for privacy and time to themselves is much
     greater than for individuals who score high on this scale. Your level of
     gregariousness is $flev[8].</li>
<li> <I>Assertiveness</i>. High scorers Assertiveness like to speak out, take
     charge, and direct the activities of others. They tend to be leaders in
     groups. Low scorers tend not to talk much and let others control the
     activities of groups. Your level of assertiveness is $flev[9].</li>
<li> <I>Activity Level</i>. Active individuals lead fast-paced, busy lives. They
     move about quickly, energetically, and vigorously, and they are involved in
     many activities. People who score low on this scale follow a slower and
     more leisurely, relaxed pace. Your activity level is $flev[10].</li>
<li> <I>Excitement-Seeking</i>. High scorers on this scale are easily bored
     without high levels of stimulation. They love bright lights and hustle and
     bustle. They are likely to take risks and seek thrills. Low scorers are
     overwhelmed by noise and commotion and are adverse to thrill-seeking.
     Your level of excitement-seeking is $flev[11].</li>
<li> <I>Cheerfulness</i>. This scale measures positive mood and feelings, not
     negative emotions (which are a part of the Neuroticism domain). Persons who
     score high on this scale typically experience a range of positive feelings,
     including happiness, enthusiasm, optimism, and joy. Low scorers are not as
     prone to such energetic, high spirits. Your level of positive emotions is
     $flev[12].</li>
</ul>
ENDOFTEXT

  print <<ENDOFTEXT;

<H2>Agreeableness</h2>

Agreeableness reflects individual differences in concern with cooperation and
social harmony. Agreeable individuals value getting along with others. They are
therefore considerate, friendly, generous, helpful, and willing to compromise
their interests with others'. Agreeable people also have an optimistic view of
human nature. They believe people are basically honest, decent, and
trustworthy.<p><p>

Disagreeable individuals place self-interest above getting along with others.
They are generally unconcerned with others' well-being, and therefore are
unlikely to extend themselves for other people. Sometimes their skepticism about
others' motives causes them to be suspicious, unfriendly, and
uncooperative.<p><p>

Agreeableness is obviously advantageous for attaining and maintaining
popularity. Agreeable people are better liked than disagreeable people. On the
other hand, agreeableness is not useful in situations that require tough or
absolute objective decisions. Disagreeable people can make excellent scientists,
critics, or soldiers.<p><p>

<table>
<tr><td>DOMAIN/Facet</td><td>Score</td><td><img src='grphhead.jpg'></td></tr>
<tr><td>AGREEABLENESS</td><td>$SAP</td><td><img src='bargray.jpg' width=$WAP height='20'></td></tr>
<tr><td>..Trust</td><td>$SAFP[1]</td><td><img src='bargray.jpg' width=$WA[1] height='20'></td></tr>
<tr><td>..Morality</td><td>$SAFP[2]</td><td><img src='bargray.jpg' width=$WA[2] height='20'></td></tr>
<tr><td>..Altruism</td><td>$SAFP[3]</td><td><img src='bargray.jpg' width=$WA[3] height='20'></td></tr>
<tr><td>..Cooperation</td><td>$SAFP[4]</td><td><img src='bargray.jpg' width=$WA[4] height='20'></td></tr>
<tr><td>..Modesty</td><td>$SAFP[5]</td><td><img src='bargray.jpg' width=$WA[5] height='20'></td></tr>
<tr><td>..Sympathy</td><td>$SAFP[6]</td><td><img src='bargray.jpg' width=$WA[6] height='20'></td></tr>
</table>

ENDOFTEXT

  if ($SA < $LO) {
      print <<ENDOFTEXT;
Your score on Agreeableness is low, indicating less concern with others' needs
Than with your own. People see you as tough, critical, and uncompromising.<P><P>
ENDOFTEXT
}

  if ($SA >= $LO && $SA <= $HI) {
      print <<ENDOFTEXT;
Your level of Agreeableness is average, indicating some concern with others'
Needs, but, generally, unwillingness to sacrifice yourself for others.<P><P>
ENDOFTEXT
}

  if ($SA > $HI) {
      print <<ENDOFTEXT;
Your high level of Agreeableness indicates a strong interest in others' needs
and well-being. You are pleasant, sympathetic, and cooperative.<P><P>
ENDOFTEXT
}

  print <<ENDOFTEXT;

<H3>Agreeableness Facets</h3>

<ul>
<li> <I>Trust</i>. A person with high trust assumes that most people are
     fair, honest, and have good intentions. Persons low in trust see others
     as selfish, devious, and potentially dangerous. Your level of
     trust is $flev[19].</li>
<li> <I>Morality</i>. High scorers on this scale see no need for pretense
     or manipulation when dealing with others and are therefore candid, frank,
     and sincere. Low scorers believe that a certain amount of deception in
     social relationships is necessary. People find it relatively easy to relate
     to the straightforward high-scorers on this scale. They generally find it
     more difficult to relate to the unstraightforward low-scorers on this
     scale. It should be made clear that low scorers are <U>not</u> unprincipled
     or immoral; they are simply more guarded and less willing to openly reveal
     the whole truth. Your level of morality is $flev[20].</li>
<li> <I>Altruism</i>. Altruistic people find helping other people genuinely
     rewarding. Consequently, they are generally willing to assist those who
     are in need. Altruistic people find that doing things for others is a form
     of self-fulfillment rather than self-sacrifice. Low scorers on this scale
     do not particularly like helping those in need. Requests for help feel like
     an imposition rather than an opportunity for self-fulfillment. Your level
     of altruism is $flev[21].</li>
<li> <I>Cooperation</i>. Individuals who score high on this scale dislike
     confrontations. They are perfectly willing to compromise or to deny their
     own needs in order to get along with others. Those who score low on this
     scale are more likely to intimidate others to get their way. Your
     level of compliance is $flev[22].</li>
<li> <I>Modesty</i>. High scorers on this scale do not like to claim that they
     are better than other people. In some cases this attitude may derive from
     low self-confidence or self-esteem. Nonetheless, some people with high
     self-esteem find immodesty unseemly. Those who <U>are</u> willing to
     describe themselves as superior tend to be seen as disagreeably arrogant
     by other people. Your level of modesty is $flev[23].</li>
<li> <I>Sympathy</i>. People who score high on this scale are tenderhearted
     and compassionate. They feel the pain of others vicariously and are easily
     moved to pity. Low scorers are not affected strongly by human suffering.
     They pride themselves on making objective judgments based on reason.
     They are more concerned with truth and impartial justice than with mercy.
     Your level of tender-mindedness is $flev[24].</li>
</ul>
ENDOFTEXT

  print <<ENDOFTEXT;

<H2>Conscientiousness</h2>

Conscientiousness concerns the way in which we control, regulate, and direct our impulses. Impulses are not inherently bad; occasionally time constraints require a snap decision, and acting on our first impulse can be an effective response. Also, in times of play rather than work, acting spontaneously and impulsively can be fun. Impulsive individuals can be seen by others as colorful, fun-to-be-with, and zany.<P><P>

Nonetheless, acting on impulse can lead to trouble in a number of ways. Some impulses are antisocial. Uncontrolled antisocial acts not only harm other members of society, but also can result in retribution toward the perpetrator of such impulsive acts. Another problem with impulsive acts is that they often produce immediate rewards but undesirable, long-term consequences. Examples include excessive socializing that leads to being fired from one's job, hurling an insult that causes the breakup of an important relationship, or using pleasure-inducing drugs that eventually destroy one's health.<P><P>

Impulsive behavior, even when not seriously destructive, diminishes a person's effectiveness in significant ways. Acting impulsively disallows contemplating alternative courses of action, some of which would have been wiser than the impulsive choice. Impulsivity also sidetracks people during projects that require organized sequences of steps or stages. Accomplishments of an impulsive person are therefore small, scattered, and inconsistent.<P><P>

A hallmark of intelligence, what potentially separates human beings from earlier life forms, is the ability to think about future consequences before acting on an impulse. Intelligent activity involves contemplation of long-range goals, organizing and planning routes to these goals, and persisting toward one's goals in the face of short-lived impulses to the contrary. The idea that intelligence involves impulse control is nicely captured by the term prudence, an alternative label for the Conscientiousness domain. Prudent means both wise and cautious. Persons who score high on the Conscientiousness scale are, in fact, perceived by others as intelligent.<P><P>

The benefits of high conscientiousness are obvious. Conscientious individuals avoid trouble and achieve high levels of success through purposeful planning and persistence. They are also positively regarded by others as intelligent and reliable. On the negative side, they can be compulsive perfectionists and workaholics. Furthermore, extremely conscientious individuals might be regarded as stuffy and boring. Unconscientious people may be criticized for their unreliability, lack of ambition, and failure to stay within the lines, but they will experience many short-lived pleasures and they will never be called stuffy.<p><p>

<table>
<tr><td>DOMAIN/Facet</td><td>Score</td><td><img src='grphhead.jpg'></td></tr>
<tr><td>CONSCIENTIOUSNESS</td><td>$SCP</td><td><img src='bargray.jpg' width=$WCP height='20'></td></tr>
<tr><td>..Self-Efficacy</td><td>$SCFP[1]</td><td><img src='bargray.jpg' width=$WC[1] height='20'></td></tr>
<tr><td>..Orderliness</td><td>$SCFP[2]</td><td><img src='bargray.jpg' width=$WC[2] height='20'></td></tr>
<tr><td>..Dutifulness</td><td>$SCFP[3]</td><td><img src='bargray.jpg' width=$WC[3] height='20'></td></tr>
<tr><td>..Achievement-Striving</td><td>$SCFP[4]</td><td><img src='bargray.jpg' width=$WC[4] height='20'></td></tr>
<tr><td>..Self-Discipline</td><td>$SCFP[5]</td><td><img src='bargray.jpg' width=$WC[5] height='20'></td></tr>
<tr><td>..Cautiousness</td><td>$SCFP[6]</td><td><img src='bargray.jpg' width=$WC[6] height='20'></td></tr>
</table>
ENDOFTEXT

  if ($SC < $LO) {
      print <<ENDOFTEXT;
Your score on Conscientiousness is low, indicating you like to live for the moment and do what feels good now. Your work tends to be careless and disorganized. <P><P>
ENDOFTEXT
}

  if ($SC >= $LO && $SC <= $HI) {
      print <<ENDOFTEXT;
Your score on Conscientiousness is average. This means you are reasonably reliable, organized, and self-controlled. <P><P>
ENDOFTEXT
}

  if ($SC > $HI) {
      print <<ENDOFTEXT;
Your score on Conscientiousness is high. This means you set clear goals and pursue them with determination. People regard you as reliable and hard-working. <P><P>
ENDOFTEXT
}

  print <<ENDOFTEXT;

<H3>Conscientiousness Facets</h3>

<ul>
<li> <I>Self-Efficacy</i>. Self-Efficacy describes confidence in one's ability
     to accomplish things. High scorers believe they have the intelligence
     (common sense), drive, and self-control necessary for achieving success.
     Low scorers do not feel effective, and may have a sense that they are not
     in control of their lives. Your level of self-efficacy is $flev[25].</li>
<li> <I>Orderliness</i>. Persons with high scores on orderliness are
     well-organized. They like to live according to routines and schedules. They
     keep lists and make plans. Low scorers tend to be disorganized and
     scattered. Your level of orderliness is $flev[26].</li>
<li> <I>Dutifulness</i>. This scale reflects the strength of a person's sense
     of duty and obligation. Those who score high on this scale have a strong
     sense of moral obligation. Low scorers find contracts, rules, and
     regulations overly confining. They are likely to be seen as unreliable or
     even irresponsible. Your level of dutifulness is $flev[27].</li>
<li> <I>Achievement-Striving</i>. Individuals who score high on this
     scale strive hard to achieve excellence. Their drive to be recognized as
     successful keeps them on track toward their lofty goals. They often have
     a strong sense of direction in life, but extremely high scores may
     be too single-minded and obsessed with their work. Low scorers are content
     to get by with a minimal amount of work, and might be seen by others
     as lazy. Your level of achievement striving is $flev[28].</li>
<li> <I>Self-Discipline</i>. Self-discipline-what many people call 
     will-power-refers to the ability to persist at difficult or unpleasant
     tasks until they are completed. People who possess high self-discipline
     are able to overcome reluctance to begin tasks and stay on track despite
     distractions. Those with low self-discipline procrastinate and show poor
     follow-through, often failing to complete tasks-even tasks they want very
     much to complete. Your level of self-discipline is $flev[29].</li>
<li> <I>Cautiousness</i>. Cautiousness describes the disposition to
     think through possibilities before acting. High scorers on the Cautiousness
     scale take their time when making decisions. Low scorers often say or do
     first thing that comes to mind without deliberating alternatives and the
     probable consequences of those alternatives. Your level
     of cautiousness is $flev[30].</li>
</ul>
ENDOFTEXT

  ($LO = 45);
  ($HI = 55);

  print <<ENDOFTEXT;

<H2>Neuroticism</h2>

Freud originally used the term <I>neurosis</I> to describe a condition marked by mental distress, emotional suffering, and an inability to cope effectively with the normal demands of life. He suggested that everyone shows some signs of neurosis, but that we differ in our degree of suffering and our specific symptoms of distress. Today neuroticism refers to the tendency to experience negative feelings. Those who score high on Neuroticism may experience primarily one specific negative feeling such as anxiety, anger, or depression, but are likely to experience several of these emotions. People high in neuroticism are emotionally reactive. They respond emotionally to events that would not affect most people, and their reactions tend to be more intense than normal. They are more likely to interpret ordinary situations as threatening, and minor frustrations as hopelessly difficult. Their negative emotional reactions tend to persist for unusually long periods of time, which means they are often in a bad mood. These problems in emotional regulation can diminish a neurotic's ability to think clearly, make decisions, and cope effectively with stress.<p><p>

At the other end of the scale, individuals who score low in neuroticism are less easily upset and are less emotionally reactive. They tend to be calm, emotionally stable, and free from persistent negative feelings. Freedom from negative feelings does not mean that low scorers experience a lot of positive feelings; frequency of positive emotions is a component of the Extraversion domain.<p><p>

<table>
<tr><td>DOMAIN/Facet</td><td>Score</td><td><img src='grphhead.jpg'></td></tr>
<tr><td>NEUROTICISM</td><td>$SNP</td><td><img src='bargray.jpg' width=$WNP height='20'></td></tr>
<tr><td>..Anxiety</td><td>$SNFP[1]</td><td><img src='bargray.jpg' width=$WN[1] height='20'></td></tr>
<tr><td>..Anger</td><td>$SNFP[2]</td><td><img src='bargray.jpg' width=$WN[2] height='20'></td></tr>
<tr><td>..Depression</td><td>$SNFP[3]</td><td><img src='bargray.jpg' width=$WN[3] height='20'></td></tr>
<tr><td>..Self-Consciousness</td><td>$SNFP[4]</td><td><img src='bargray.jpg' width=$WN[4] height='20'></td></tr>
<tr><td>..Immoderation</td><td>$SNFP[5]</td><td><img src='bargray.jpg' width=$WN[5] height='20'></td></tr>
<tr><td>..Vulnerability</td><td>$SNFP[6]</td><td><img src='bargray.jpg' width=$WN[6] height='20'></td></tr>
</table>
ENDOFTEXT

  if ($SN < $LO) {
      print <<ENDOFTEXT;
Your score on Neuroticism is low, indicating that you are exceptionally calm, composed and unflappable. You do not react with intense emotions, even to situations that most people would describe as stressful.<P><P>
ENDOFTEXT
}

  if ($SN >= $LO && $SN <= $HI) {
      print <<ENDOFTEXT;
Your score on Neuroticism is average, indicating that your level of emotional reactivity is typical of the general population. Stressful and frustrating situations are somewhat upsetting to you, but you are generally able to get over these feelings and cope with these situations.<P><P>
ENDOFTEXT
}

  if ($SN > $HI) {
      print <<ENDOFTEXT;
Your score on Neuroticism is high, indicating that you are easily upset, even by what most people consider the normal demands of living. People consider you to be sensitive and emotional.<P><P>
ENDOFTEXT
}

  print <<ENDOFTEXT;

<H3>Neuroticism Facets</h3>

<ul>
<li> <I>Anxiety</i>. The "fight-or-flight" system of the brain of anxious
     individuals is too easily and too often engaged. Therefore, people who
     are high in anxiety often feel like something dangerous is about to happen.
     They may be afraid of specific situations or be just generally fearful.
     They feel tense, jittery, and nervous. Persons low in Anxiety are generally
     calm and fearless. Your level of anxiety is $flev[1].</li>
<li> <I>Anger</i>. Persons who score high in Anger feel enraged when
     things do not go their way. They are sensitive about being treated fairly
     and feel resentful and bitter when they feel they are being cheated.
     This scale measures the tendency to <I>feel</I> angry; whether or not the
     person <I>expresses</I> annoyance and hostility depends on the individual's
     level on Agreeableness. Low scorers do not get angry often or easily.
     Your level of anger is $flev[2].</li>
<li> <I>Depression</i>. This scale measures the tendency to feel sad, dejected,
     and discouraged. High scorers lack energy and have difficult initiating
     activities. Low scorers tend to be free from these depressive feelings.
     Your level of depression is $flev[3].</li>
<li> <I>Self-Consciousness</i>. Self-conscious individuals are sensitive
     about what others think of them. Their concern about rejection and
     ridicule cause them to feel shy and uncomfortable abound others. They
     are easily embarrassed and often feel ashamed. Their fears that others
     will criticize or make fun of them are exaggerated and unrealistic, but
     their awkwardness and discomfort may make these fears a self-fulfilling
     prophecy. Low scorers, in contrast, do not suffer from the mistaken
     impression that everyone is watching and judging them. They do not feel
     nervous in social situations. Your level or self-consciousness is
     $flev[4].</li>
<li> <I>Immoderation</i>. Immoderate individuals feel strong cravings and
     urges that they have have difficulty resisting. They tend to be
     oriented toward short-term pleasures and rewards rather than long-
     term consequences. Low scorers do not experience strong, irresistible
     cravings and consequently do not find themselves tempted to overindulge.
     Your level of immoderation is $flev[5].</li>
<li> <I>Vulnerability</i>. High scorers on Vulnerability experience panic,
     confusion, and helplessness when under pressure or stress. Low scorers
     feel more poised, confident, and clear-thinking when stressed.
     Your level of vulnerability is $flev[6].</li>
</ul>
ENDOFTEXT

print <<ENDOFTEXT;

<H2>Openness to Experience</h2>

Openness to Experience describes a dimension of cognitive style that
distinguishes imaginative, creative people from down-to-earth, conventional
people. Open people are intellectually curious, appreciative of art, and
sensitive to beauty. They tend to be, compared to closed people, more aware of
their feelings. They tend to think and act in individualistic and nonconforming
ways. Intellectuals typically score high on Openness to Experience;
consequently, this factor has also been called <I>Culture</I> or
<I>Intellect</I>. Nonetheless, Intellect is probably best regarded as one aspect of openness
to experience. Scores on Openness to Experience are only modestly
related to years of education and scores on standard intelligent tests.<p><p>

Another characteristic of the open cognitive style is a facility for thinking
in symbols and abstractions far removed from concrete experience. Depending on
the individual's specific intellectual abilities, this symbolic cognition may
take the form of mathematical, logical, or geometric thinking, artistic and
metaphorical use of language, music composition or performance, or one of the
many visual or performing arts.

People with low scores on openness to experience tend to have narrow, common
interests. They prefer the plain, straightforward, and obvious over the
complex, ambiguous, and subtle. They may regard the arts and sciences with
suspicion, regarding these endeavors as abstruse or of no practical use.
Closed people prefer familiarity over novelty; they are conservative and
resistant to change.<p><p>

Openness is often presented as healthier or more mature by psychologists, who
are often themselves open to experience. However, open and closed styles of
thinking are useful in different environments. The intellectual style of the
open person may serve a professor well, but research has shown that closed
thinking is related to superior job performance in police work, sales, and
a number of service occupations.<p><p>

<table>
<tr><td>DOMAIN/Facet</td><td>Score</td><td><img src='grphhead.jpg'></td></tr>
<tr><td>OPENNESS</td><td>$SOP</td><td><img src='bargray.jpg' width=$WOP height='20'></td></tr>
<tr><td>..Imagination</td><td>$SOFP[1]</td><td><img src='bargray.jpg' width=$WO[1] height='20'></td></tr>
<tr><td>..Artistic Interests</td><td>$SOFP[2]</td><td><img src='bargray.jpg' width=$WO[2] height='20'></td></tr>
<tr><td>..Emotionality</td><td>$SOFP[3]</td><td><img src='bargray.jpg' width=$WO[3] height='20'></td></tr>
<tr><td>..Adventurousness</td><td>$SOFP[4]</td><td><img src='bargray.jpg' width=$WO[4] height='20'></td></tr>
<tr><td>..Intellect</td><td>$SOFP[5]</td><td><img src='bargray.jpg' width=$WO[5] height='20'></td></tr>
<tr><td>..Liberalism</td><td>$SOFP[6]</td><td><img src='bargray.jpg' width=$WO[6] height='20'></td></tr>
</table>
ENDOFTEXT

  if ($SO < $LO ) {
      print <<ENDOFTEXT;
Your score on Openness to Experience is low, indicating you like to think in
plain and simple terms. Others describe you as down-to-earth, practical,
and conservative.<P><P>
ENDOFTEXT
}

  if ($SO >= $LO && $SO <= $HI) {
      print <<ENDOFTEXT;
Your score on Openness to Experience is average, indicating you enjoy tradition
but are willing to try new things. Your thinking is neither simple nor
complex. To others you appear to be a well-educated person but not an intellectual.<P><P>
ENDOFTEXT
}

  if ($SO > $HI) {
      print <<ENDOFTEXT;
Your score on Openness to Experience is high, indicating you enjoy novelty,
variety, and change. You are curious, imaginative, and creative.<P><P>
ENDOFTEXT
}
  print <<ENDOFTEXT;

<H3>Openness Facets</h3>

<ul>
<li> <I>Imagination</i>. To imaginative individuals, the real world is
     often too plain and ordinary. High scorers on this scale use fantasy as a
     way of creating a richer, more interesting world. Low scorers are on this
     scale are more oriented to facts than fantasy. Your level of imagination
     is $flev[13].</li>
<li> <I>Artistic Interests</i>. High scorers on this scale love beauty, both in
     art and in nature. They become easily involved and absorbed in artistic
     and natural events. They are not necessarily artistically trained nor
     talented, although many will be. The defining features of this scale are
     <I>interest in</I>, and <I>appreciation of</I> natural and
     artificial beauty. Low scorers lack aesthetic sensitivity and interest in
     the arts. Your level of artistic interests is $flev[14].</li>
<li> <I>Emotionality</i>. Persons high on Emotionality have good access
     to and awareness of their own feelings. Low scorers are less aware of
     their feelings and tend not to express their emotions openly. Your
     level of emotionality is $flev[15].</li>
<li> <I>Adventurousness</i>. High scorers on adventurousness are eager to
     try new activities, travel to foreign lands, and experience different
     things. They find familiarity and routine boring, and will take a new
     route home just because it is different. Low scorers tend to feel
     uncomfortable with change and prefer familiar routines. Your level of
     adventurousness is $flev[16].</li>
<li> <I>Intellect</i>. Intellect and artistic interests are the two most
     important, central aspects of openness to experience. High scorers on
     Intellect love to play with ideas. They are open-minded to new and unusual
     ideas, and like to debate intellectual issues. They enjoy riddles, puzzles,
     and brain teasers. Low scorers on Intellect prefer dealing with either
     people or things rather than ideas. They regard intellectual exercises as a
     waste of time. Intellect should <U>not</u> be equated with intelligence.
     Intellect is an intellectual style, not an intellectual ability, although
     high scorers on Intellect score <U>slightly</u> higher than low-Intellect
     individuals on standardized intelligence tests. Your level of intellect
     is $flev[17].</li>
<li> <I>Liberalism</i>. Psychological liberalism refers to a readiness to
     challenge authority, convention, and traditional values. In its most
     extreme form, psychological liberalism can even represent outright
     hostility toward rules, sympathy for law-breakers, and love of ambiguity,
     chaos, and disorder. Psychological conservatives prefer the security and
     stability brought by conformity to tradition. Psychological liberalism
     and conservatism are not identical to political affiliation, but certainly
     incline individuals toward certain political parties. Your level of
     liberalism is $flev[18].</li>
</ul>
ENDOFTEXT

print $query->end_html;
}