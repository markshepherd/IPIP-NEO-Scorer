#!/usr/bin/perl

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

# Check to see that sex was indicated
  if ($Sex ne "Male" && $Sex ne "Female") {
  print $query->header;
  print $query->start_html(-title=>'Failure to Indicate Sex');
  print "You did not indicate your sex at the beginning of the inventory. Your answers 
cannot be normed properly unless you indicate whether you are male or female.
Please return to the inventory and indicate your sex.";
  exit;
}

#Make sure Age is numeric
  if ($Age =~ /\D/) {
  print $query->header;
  print $query->start_html(-title=>'Invalid, Non-numeric Entry for Age');
    print "You did not enter your age in numeric digits. For example if you have lived for three decades, you must enter 30 rather than thirty in the Age box. Please return to the previous page and enter your age properly.";
  exit;
}

#Make sure respondent is at least 10 years old
  if ($Age < 10) {
  print $query->header;
  print $query->start_html(-title=>'Age in Invalid Range');
  print "You did not indicate how old you are at the beginning of the inventory, or you 
typed in an age that is too young. Your answers cannot be normed properly
unless you type in a valid age. Please return to the inventory and change your response.";
  exit;
}
  if ($Age > 99) {
    print "Are you really as old as you have indicated? If you really are that old, congratulations on living so long! But to make data processing easier, I want to limit ages to two-digit numbers. If you really are 100 years old or older, please return to the previous page and enter a 99 for your age.";
  exit;
}

  if ($Country !~ /\w/) {
  print $query->header;
  print $query->start_html(-title=>'Country Not Indicated');
    print "You did not indicate which country you are from. Indicating where you are from will help build better norms that will improve the validity of this test. Please return to the previous page and indicate the country to which you feel you belong the most.";
  exit;
}

#Generate random nickname if nickname is blank
    if ($Nick !~ /\w/) {
    $Nick = &random_password(23); 
}

#Truncate long Nicknames
$str_length = length($Nick);
  if ($str_length > 23) {
  ($Nick = substr($Nick, 0, 23));
}

#Pad short Nicknames
  $blank_str = " ";
  while ($str_length < 23) {
  $Nick .= $blank_str;
  $str_length = length($Nick);
}

 
# Get the item responses
  for ($i = 1; $i < 61; $i++) {
  $item = "Q$i";
  $Q[$i] = $query->param($item);
}

# Print the header and start HTML
  print $query->header;
  print $query->start_html(
  -title=>'IPIP-NEO-PI Short Form Items 61-120');


  print <<ENDOFTEXT;

  <form method=post action="shortipipneo3.cgi">
ENDOFTEXT

  print "<input type=\"hidden\" name=\"Nick\" value=\"$Nick\">\n";
  print "<input type=\"hidden\" name=\"Sex\" value=\"$Sex\">\n";
  print "<input type=\"hidden\" name=\"Age\" value=\"$Age\">\n";
  print "<input type=\"hidden\" name=\"Country\" value=\"$Country\">\n";
  for ($i = 1; $i < 61; $i++) {
  print "<input type=\"hidden\" name=\"Q$i\" value=\"$Q[$i]\">\n";
}
  print <<ENDOFTEXT;
<table border>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>61. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am afraid of many things.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q61" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q61" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q61" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q61" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q61" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>62. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Avoid contacts with others.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q62" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q62" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q62" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q62" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q62" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>63. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Love to daydream.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q63" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q63" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q63" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q63" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q63" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>64. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Trust what people say.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q64" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q64" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q64" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q64" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q64" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>65. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Handle tasks smoothly.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q65" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q65" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q65" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q65" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q65" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>66. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Lose my temper.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q66" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q66" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q66" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q66" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q66" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>67. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Prefer to be alone.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q67" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q67" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q67" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q67" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q67" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>68. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Do not like poetry.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q68" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q68" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q68" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q68" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q68" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>69. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Take advantage of others.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q69" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q69" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q69" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q69" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q69" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>70. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Leave a mess in my room.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q70" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q70" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q70" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q70" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q70" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>71. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am often down in the dumps.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q71" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q71" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q71" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q71" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q71" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>72. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Take control of things.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q72" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q72" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q72" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q72" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q72" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>73. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Rarely notice my emotional reactions.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q73" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q73" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q73" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q73" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q73" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>74. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am indifferent to the feelings of others.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q74" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q74" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q74" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q74" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q74" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>75. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Break rules.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q75" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q75" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q75" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q75" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q75" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>76. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Only feel comfortable with friends.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q76" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q76" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q76" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q76" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q76" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>77. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Do a lot in my spare time.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q77" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q77" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q77" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q77" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q77" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>78. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Dislike changes.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q78" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q78" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q78" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q78" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q78" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>79. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Insult people.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q79" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q79" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q79" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q79" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q79" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>80. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Do just enough work to get by.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q80" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q80" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q80" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q80" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q80" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>81. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Easily resist temptations.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q81" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q81" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q81" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q81" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q81" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>82. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Enjoy being reckless.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q82" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q82" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q82" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q82" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q82" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>83. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Have difficulty understanding abstract ideas.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q83" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q83" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q83" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q83" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q83" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>84. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Have a high opinion of myself.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q84" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q84" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q84" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q84" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q84" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>85. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Waste my time.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q85" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q85" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q85" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q85" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q85" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>86. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Feel that I'm unable to deal with things.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q86" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q86" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q86" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q86" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q86" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>87. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Love life.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q87" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q87" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q87" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q87" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q87" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>88. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Tend to vote for conservative political candidates.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q88" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q88" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q88" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q88" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q88" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>89. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am not interested in other people's problems.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q89" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q89" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q89" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q89" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q89" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>90. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Rush into things.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q90" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q90" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q90" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q90" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q90" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>91. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Get stressed out easily.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q91" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q91" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q91" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q91" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q91" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>92. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Keep others at a distance.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q92" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q92" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q92" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q92" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q92" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>93. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Like to get lost in thought.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q93" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q93" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q93" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q93" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q93" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>94. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Distrust people.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q94" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q94" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q94" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q94" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q94" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>95. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Know how to get things done.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q95" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q95" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q95" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q95" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q95" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>96. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am not easily annoyed.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q96" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q96" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q96" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q96" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q96" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>97. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Avoid crowds.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q97" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q97" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q97" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q97" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q97" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>98. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Do not enjoy going to art museums.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q98" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q98" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q98" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q98" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q98" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>99. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Obstruct others' plans.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q99" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q99" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q99" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q99" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q99" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>100. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Leave my belongings around.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q100" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q100" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q100" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q100" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q100" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>101. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Feel comfortable with myself.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q101" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q101" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q101" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q101" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q101" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>102. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Wait for others to lead the way.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q102" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q102" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q102" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q102" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q102" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>103. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Don't understand people who get emotional.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q103" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q103" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q103" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q103" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q103" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>104. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Take no time for others.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q104" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q104" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q104" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q104" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q104" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>105. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Break my promises.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q105" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q105" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q105" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q105" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q105" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>106. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am not bothered by difficult social situations.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q106" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q106" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q106" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q106" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q106" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>107. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Like to take it easy.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q107" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q107" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q107" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q107" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q107" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>108. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am attached to conventional ways.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q108" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q108" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q108" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q108" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q108" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>109. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Get back at others.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q109" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q109" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q109" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q109" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q109" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>110. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Put little time and effort into my work.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q110" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q110" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q110" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q110" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q110" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>111. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am able to control my cravings.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q111" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q111" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q111" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q111" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q111" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>112. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Act wild and crazy.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q112" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q112" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q112" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q112" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q112" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>113. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am not interested in theoretical discussions.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q113" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q113" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q113" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q113" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q113" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>114. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Boast about my virtues.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q114" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q114" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q114" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q114" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q114" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>115. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Have difficulty starting tasks.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q115" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q115" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q115" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q115" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q115" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>116. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Remain calm under pressure.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q116" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q116" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q116" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q116" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q116" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>117. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Look at the bright side of life.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q117" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q117" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q117" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q117" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q117" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>118. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Believe that we should be tough on crime.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q118" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q118" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q118" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q118" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q118" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>119. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Try not to think about the needy.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q119" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q119" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q119" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q119" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q119" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>120. </TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Act without thinking.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q120" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q120" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate<BR>
nor Inaccurate<BR>

<INPUT TYPE="RADIO" NAME="Q120" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q120" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very<BR>
Accurate<BR>

<INPUT TYPE="RADIO" NAME="Q120" VALUE="1">
</center></td>
</TR>
</TABLE>

<b>PLEASE NOTE:</b> Your results should appear on your screen within moments after clicking the Send button. If nothing happens, something has gone wrong. Clicking the button again and again will not help.</p>
<p>
As I indicated in the warning at the beginning of the test, I am a psychologist, not a computer technician, so I have no definitive way of solving any person's particular computer problem.  For people who were unable to complete the test, sometimes using a better computer, faster internet connection, or just taking the test on a different day and time led to success. If you experience difficulties, you can email me if you like (j5j at psu.edu), but I won't be able to tell you anything more than what I have just said here.</p>
<p><br><input type="submit" value="Send "><b>&nbsp;&nbsp;This 
will send your answers to be scored and post your results.</b>
</form>
ENDOFTEXT
print $query->end_html;
}
# Name:      random_password()
#
# Author:    Chris Hunt
#
# Date:      May 1999
#
# Purpose:   Returns a random word for use as a password. Consonants and vowels
#            are alternated to give a (hopefully) pronouncable, and hence
#            memorable, result.
#
# Arguments: The single (optional) argument sets the approximate length of the
#            word. Use of dipthongs (two-letter combinations) may make the word
#            exceed this length by 1. If the argument is omitted, a default
#            value (6) is assumed.
#
# Usage:     $my_new_password  = &random_password();
#            $my_long_password = &random_password(10);
#
# (c)1999 Chris Hunt. Permission is freely granted to include this script in
# your programs. provided this header is left intact.
#
# The latest version of this script can be found at http://www.extracon.com
#

sub random_password {

   ($maxlen) = $_[0] || 6;   # Default to 6

   # Build tables of vowels & consonants. Single vowels are repeated so that
   # resultant words are not dominated by dipthongs

   (@vowel) = ("a", "a", "a", "e", "e", "e", "e", "i", "i", "i", 
          "o", "o", "o", "u", "u", "y", "ai", "au", "ay", "ea",
          "ee", "eu", "ia", "ie", "io", "oa", "oi", "oo", "oy");
   (@consonant) = ("b", "c", "d", "f", "g", "h", "j", "k", "l", 
          "m", "n", "p", "qu", "r", "s", "t", "v", "w", "x", "z", "th", "st",
          "sh", "ph", "ng", "nd");
   ($password) = "";

   srand;                 
   ($vowelnext) = int(rand(2));  # Initialise to 0 or 1 (ie true or false)

   do {
      if ($vowelnext) {
         $password .= $vowel[rand(@vowel)];
      } else {
         $password .= $consonant[rand(@consonant)];
      }

      $vowelnext = !$vowelnext;    # Swap letter type for the next one

   } until length($password) >= $maxlen;

   return $password;

}
