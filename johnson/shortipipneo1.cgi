#!/usr/bin/perl
use CGI;

# Read in identifying information
  $query = new CGI;

# Extract acknowledgement variables
  $Risk = $query->param('Risk');
  $Accuracy = $query->param('Accuracy');

  if ($Risk ne "Yes") {
  print $query->header;
  print $query->start_html(-title=>'Failure to Acknowledge Risks');
  print "You did not acknowledge that you understand that responding to all items on this inventory is time consuming and that sometimes technical difficulties prevent the results from being displayed. To access the test you must return to the previous page and click the answer circle indictating that you are responding to this inventory with the full knowledge of the risk that you might not receive results and that you accept full responsibility and risk for the time you invest in responding to this inventory.";
  exit;
}

  if ($Accuracy ne "Yes") {
# Print the header
  print $query->header;
  print $query->start_html(-title=>'Failure to Acknowledge Test Limitations');
  print "You did not indicate you understand that this inventory is designed to accurately and objectively estimate your standing on personality traits that are obvious to most people who know me well. To access the test you must return to the previous page and click the answer circle indicating that if you think you have answered the items honestly and carefully but your results are inaccurate or not as pleasing as you would like them to be, you will have knowledgeable acquaintances evaluate the validity of the report before contacting Dr. Johnson. Clicking the answer circle also indicates that if you choose to critique the test or narrative report after receiving feedback from knowledgeable acquaintances, you will do so in a courteous and civil manner.";
  exit;
}

# Assign form validating JavaScript to variable

  $jscript=<<END;
function debug(formObject){
	formObject.Nick.value="debug";
	formObject.Sex[0].checked=true;
	formObject.Age.value=25;
	formObject.Country.value="USA";
	for (var i=1; i <= 60; i++)
		{
		radObject=formObject.elements["Q"+i];
		radObject[2].checked=true;
		}
	}
	
function validate(formObject) {
	// reset everything
	err=false;
	document.getElementById("nameError").style.display = "none";
	document.getElementById("sexError").style.display = "none";
	document.getElementById("ageError").style.display = "none";
	document.getElementById("countryError").style.display = "none";
	
	// check name, gender, age, country
	if (formObject.Nick.value.length == 0)
    {
		document.getElementById("nameError").style.display = "inline";
        formObject.Nick.focus();
        err=true;
    }
	if (!isChecked(formObject.Sex))
    {
		document.getElementById("sexError").style.display = "inline";
        formObject.Sex[0].focus();
        err=true;
    }
	
	if (isNaN(formObject.Age.value) || formObject.Age.value.length == 0)
    {
		document.getElementById("ageError").style.display = "inline";
        formObject.Age.focus();
        err=true;
    }
	
	if (formObject.Country.value == "")
    {
		document.getElementById("countryError").style.display = "inline";
        formObject.Country.focus();
        err=true;
    }
	
	if (err) {
		return false;
	} else {
		// check all 60 radio buttons
		foc=0;
		message="Please make sure you have answered all of the questions. The following were not answered: ";
		for (var i=1; i <= 60; i++)
		{
		if (!isChecked(formObject.elements["Q"+i]))
			{
			if (foc==0) {
				err=true; 
				foc=i; 
				message+=i;
			} else {
			message+=", " + i;
			}
			}
		}
		if (err) {
			alert(message);
			foc=foc*5;
			formObject.elements[foc].focus();
			return false;
		}
    	}
}
function isChecked(radGroup){
	for (var i=0;i<radGroup.length;i++){
	if (radGroup[i].checked) return true;
	}
	return false;
}
END

# Print the header and start HTML
  print $query->header;
  print $query->start_html(
  -title=>'IPIP-NEO-PI Short Form Items 1-60',
  -script=>$jscript);

  print <<ENDOFTEXT;
<div id="main">
<h2>
Instructions for Completing the IPIP-NEO Short Form</h2>
The following pages contain phrases describing people's behaviors. Please
use the rating scale next to each phrase to describe how accurately each
statement describes you. Describe yourself as you generally are now, not
as you wish to be in the future. Describe yourself as you honestly see
yourself, in relation to other people you know of the same sex as you are,
and roughly your same age. So that you can describe yourself in an honest
manner, your responses will be kept in absolute confidence. Please read
each statement carefully, and then click the circle that corresponds to
the accuracy of the statement.
<p>Answer every item. Failing to answer items will return an invalid narrative
report. Note that the answer circles appear directly to the right of each
question. Please make sure that the circle you are choosing corresponds
to the question you are considering. If you make a mistake or change your
mind, simply click the circle you wish to choose. After you have answered
the first 60 of the 120 total items, press the send button. at the bottom
of this page. This will send your responses to the scoring program and
take you to a page with the next 60 questions. After you complete this second page of 60 questions, pressing the send button will return an interpretive
report to you.

<p>All responses to this inventory from all respondents are completely
confidential and will <b><u>not</u></b> be associated with you as an individual.
Responses are, however, automatically entered into a database in order
to improve norms by age and sex and to assess the statistical properties
of item responses for groups of respondents. To ensure confidentiality of your responses to the inventory, <b>DO
NOT</b> enter your real name in the box below. Please use a nickname or
made-up name. If you do not enter a nickname with at least one letter or numeral in it, a random nickname will be generated for you.

<form method=post action="shortipipneo2.cgi" name="part1" onSubmit="return validate(part1);">
<!-- For debugging - fills in all fields -->
<!-- <a href="#" onClick="return debug(part1);">Debug</a> -->

<p><font size=+2>Your Nickname or Made-up Name</font><input NAME="Nick" VALUE="" size=50>
<br>&nbsp;
<p><u><font color="#FF0000"><font size=+1>This inventory will not be scored
unless valid values for sex, age, and country are entered.</font></font></u>
<br>&nbsp;
<br>&nbsp;
<table><tr>
<td WIDTH="50"><strong>Sex:</strong></td>
<td WIDTH="70" align="center"><b>Male</b>
<br><input TYPE="RADIO" NAME="Sex" VALUE="Male"></td>
<td WIDTH="70" align="center"><b>Female</b>
<br><input TYPE="RADIO" NAME="Sex" VALUE="Female"></td>
</tr></table>
<span class="error" id="sexError">Please select Male or Female before continuing.</span>


<p><font size=+2>Age:</font><input NAME="Age" VALUE="" size=5 maxlength=2>
<span class="error" id="ageError">Please enter your age (in years) before continuing. You must be 18 years or older.</span>

<p>When selecting your country, please indicate the country to which you feel you belong the most, whether by virtue of citizenship, length of residence, or acculturation.
<p><font size=+2>Country:</font><select name="Country">
<option value="">Select Your Country
<option value="">------------------------
<option value="USA">USA
<option value="Afghanistan">Afghanistan
<option value="Albania">Albania
<option value="Algeria">Algeria
<option value="Andorra">Andorra
<option value="Angola">Angola
<option value="Anguilla">Anguilla
<option value="Antarctica">Antarctica
<option value="Antigua">Antigua
<option value="Arabian Gulf">Arabian Gulf
<option value="Argentina">Argentina
<option value="Armenia">Armenia
<option value="Aruba">Aruba
<option value="Australia">Australia
<option value="Austria">Austria
<option value="Azerbaijan">Azerbaijan
<option value="Bahamas">Bahamas
<option value="Bahrain">Bahrain
<option value="Bangladesh">Bangladesh
<option value="Barbados">Barbados
<option value="Belarus">Belarus
<option value="Belgium">Belgium
<option value="Belize">Belize
<option value="Benin">Benin
<option value="Bermuda">Bermuda
<option value="Bhutan">Bhutan
<option value="Bolivia">Bolivia
<option value="Borneo">Borneo
<option value="Bosnia Herzogovinia">Bosnia Herzogovinia
<option value="Botswana">Botswana
<option value="Bouvet Island">Bouvet Island
<option value="Brazil">Brazil
<option value="British Indian Ocean Territory">British Indian Ocean Territory
<option value="British Virgin Islands">British Virgin Islands
<option value="Brunei">Brunei
<option value="Bulgaria">Bulgaria
<option value="Burkina Fasso">Burkina Fasso
<option value="Burma">Burma
<option value="Burma(Myanmar)">Burma(Myanmar)
<option value="Burundi">Burundi
<option value="Cambodia">Cambodia
<option value="Cameroon">Cameroon
<option value="Canada">Canada
<option value="Cape Verde">Cape Verde
<option value="Cayman Islands">Cayman Islands
<option value="Central African Republic">Central African Republic
<option value="Chad">Chad
<option value="Chile">Chile
<option value="China">China
<option value="Christmas Island (Australia)">Christmas Island (Australia)
<option value="Cocos (Keeling) Islands">Cocos (Keeling) Islands
<option value="Colombia">Colombia
<option value="Comoros">Comoros
<option value="Congo">Congo
<option value="Cook Islands">Cook Islands
<option value="Costa Rica">Costa Rica
<option value="Croatia">Croatia
<option value="Cuba">Cuba
<option value="Cyprus">Cyprus
<option value="Czech Republic">Czech Republic
<option value="Denmark">Denmark
<option value="Djibouti">Djibouti
<option value="Dominica">Dominica
<option value="Dominican Republic">Dominican Republic
<option value="East Timor">East Timor
<option value="Ecuador">Ecuador
<option value="Egypt">Egypt
<option value="El Salvador">El Salvador
<option value="Equatorial Guinea">Equatorial Guinea
<option value="Eritrea">Eritrea
<option value="Estonia">Estonia
<option value="Ethiopia">Ethiopia
<option value="Faeroe Islands">Faeroe Islands
<option value="Falkland Islands">Falkland Islands
<option value="Fiji">Fiji
<option value="Finland">Finland
<option value="France">France
<option value="French Guiana">French Guiana
<option value="French Polynesia">French Polynesia
<option value="Gabon">Gabon
<option value="Gambia">Gambia
<option value="Georgia">Georgia
<option value="Germany">Germany
<option value="Ghana">Ghana
<option value="Gibraltar">Gibraltar
<option value="Greece">Greece
<option value="Greenland">Greenland
<option value="Grenada">Grenada
<option value="Guadeloupe">Guadeloupe
<option value="Guam">Guam
<option value="Guatemala">Guatemala
<option value="Guinea">Guinea
<option value="Guinea-Bissau">Guinea-Bissau
<option value="Guyana">Guyana
<option value="Haiti">Haiti
<option value="Honduras">Honduras
<option value="Hong Kong">Hong Kong
<option value="Hungary">Hungary
<option value="Iceland">Iceland
<option value="India">India
<option value="Indonesia">Indonesia
<option value="Iran">Iran
<option value="Iraq">Iraq
<option value="Ireland">Ireland
<option value="Israel">Israel
<option value="Italy">Italy
<option value="Ivory Coast">Ivory Coast
<option value="Jamaica">Jamaica
<option value="Japan">Japan
<option value="Johnston Island">Johnston Island
<option value="Jordan">Jordan
<option value="Kazakhstan">Kazakhstan
<option value="Kenya">Kenya
<option value="Kiribati">Kiribati
<option value="Kuwait">Kuwait
<option value="Kyrgystan">Kyrgystan
<option value="Lao P.Dem.R.">Lao P.Dem.R.
<option value="Latvia">Latvia
<option value="Lebanon">Lebanon
<option value="Lesotho">Lesotho
<option value="Liberia">Liberia
<option value="Libyan Arab Jamahiriya">Libyan Arab Jamahiriya
<option value="Liechtenstein">Liechtenstein
<option value="Lithuania">Lithuania
<option value="Luxembourg">Luxembourg
<option value="Macau">Macau
<option value="Macedonia">Macedonia
<option value="Madagascar">Madagascar
<option value="Malawi">Malawi
<option value="Malaysia">Malaysia
<option value="Maldives">Maldives
<option value="Mali">Mali
<option value="Malta">Malta
<option value="Marshall Islands">Marshall Islands
<option value="Martinique">Martinique
<option value="Mauritania">Mauritania
<option value="Mauritius">Mauritius
<option value="Mexico">Mexico
<option value="Micronesia">Micronesia
<option value="Midway Islands">Midway Islands
<option value="Moldova">Moldova
<option value="Monaco">Monaco
<option value="Mongolia">Mongolia
<option value="Montenegro">Montenegro
<option value="Montserrat">Montserrat
<option value="Morocco">Morocco
<option value="Mozambique">Mozambique
<option value="Namibia">Namibia
<option value="Nauru">Nauru
<option value="Nepal">Nepal
<option value="Netherlands">Netherlands
<option value="Netherlands Antilles">Netherlands Antilles
<option value="New Caledonia">New Caledonia
<option value="New Zealand">New Zealand
<option value="Nicaragua">Nicaragua
<option value="Niger">Niger
<option value="Nigeria">Nigeria
<option value="Niue">Niue
<option value="Norfolk Island">Norfolk Island
<option value="North Korea">North Korea
<option value="Northern Mariana Islands">Northern Mariana Islands
<option value="Norway">Norway
<option value="Oman">Oman
<option value="Pakistan">Pakistan
<option value="Palau">Palau
<option value="Panama">Panama
<option value="Papua New Guinea">Papua New Guinea
<option value="Paraguay">Paraguay
<option value="Peru">Peru
<option value="Philippines">Philippines
<option value="Pitcairn Islands">Pitcairn Islands
<option value="Poland">Poland
<option value="Portugal">Portugal
<option value="Puerto Rico">Puerto Rico
<option value="Qatar">Qatar
<option value="Republic of Moldavia">Republic of Moldavia
<option value="Reunion">Reunion
<option value="Romania">Romania
<option value="Russian Federation">Russian Federation
<option value="Rwanda">Rwanda
<option value="Saint Helena">Saint Helena
<option value="Saint Kitts and Nevis">Saint Kitts and Nevis
<option value="Saint Pierre and Miquelon">Saint Pierre and Miquelon
<option value="Samoa">Samoa
<option value="San Marino">San Marino
<option value="Sao Tome and Principe">Sao Tome and Principe
<option value="Saudi Arabia">Saudi Arabia
<option value="Senegal">Senegal
<option value="Serbia">Serbia
<option value="Seychelles">Seychelles
<option value="Sierra Leone">Sierra Leone
<option value="Singapore">Singapore
<option value="Slovakia">Slovakia
<option value="Slovenia">Slovenia
<option value="Solomon Islands">Solomon Islands
<option value="Somalia">Somalia
<option value="South Africa">South Africa
<option value="South Korea">South Korea
<option value="Spain">Spain
<option value="Sri Lanka">Sri Lanka
<option value="St Lucia">St Lucia
<option value="St Vincent and  Grenadines">St Vincent and  Grenadines
<option value="Sudan">Sudan
<option value="Suriname">Suriname
<option value="Svalbard &amp; Jan Mayen Islands">Svalbard & Jan Mayen Islands
<option value="Swaziland">Swaziland
<option value="Sweden">Sweden
<option value="Switzerland">Switzerland
<option value="Syria">Syria
<option value="Taiwan">Taiwan
<option value="Tajikistan">Tajikistan
<option value="Tanzania">Tanzania
<option value="Thailand">Thailand
<option value="Togo">Togo
<option value="Tokelau">Tokelau
<option value="Tonga">Tonga
<option value="Trinidad and Tobago">Trinidad and Tobago
<option value="Tunisia">Tunisia
<option value="Turkey">Turkey
<option value="Turkmenistan">Turkmenistan
<option value="Turks and Caicos Islands">Turks and Caicos Islands
<option value="Tuvalu">Tuvalu
<option value="UK">UK
<option value="USA">USA
<option value="Uganda">Uganda
<option value="Ukraine">Ukraine
<option value="United Arab Emirates">United Arab Emirates
<option value="Uruguay">Uruguay
<option value="Uzbekistan">Uzbekistan
<option value="Vanuatu">Vanuatu
<option value="Vatican">Vatican
<option value="Vatican City">Vatican City
<option value="Venezuela">Venezuela
<option value="Vietnam">Vietnam
<option value="Virgin Islands">Virgin Islands
<option value="W. Samoa">W. Samoa
<option value="Wake Island">Wake Island
<option value="Wallis and Futuna Islands">Wallis and Futuna Islands
<option value="Western Sahara">Western Sahara
<option value="Yemen">Yemen
<option value="Yugoslavia">Yugoslavia
<option value="Zaire">Zaire
<option value="Zambia">Zambia
<option value="Zimbabwe">Zimbabwe
</select>
<span class="error" id="countryError">Please select your country before continuing.</span>

<br>&nbsp;
<br>&nbsp;
<table border>
<tr>
<td VALIGN=TOP WIDTH="5%" HEIGHT="50">1.&nbsp;</td>

<td VALIGN=TOP WIDTH="28%" HEIGHT="50">Worry about things.</td>

<td VALIGN=TOP WIDTH="14%" HEIGHT="50">
<center>Very
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q1" VALUE="1"></center>
</td>

<td VALIGN=TOP WIDTH="13%" HEIGHT="50">
<center>Moderately
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q1" VALUE="2"></center>
</td>

<td VALIGN=TOP WIDTH="17%" HEIGHT="50">
<center>Neither Accurate
<br>Nor Inaccurate
<br><input TYPE="RADIO" NAME="Q1" VALUE="3"></center>
</td>

<td VALIGN=TOP WIDTH="12%" HEIGHT="50">
<center>Moderately
<br>Accurate
<br><input TYPE="RADIO" NAME="Q1" VALUE="4"></center>
</td>

<td VALIGN=TOP WIDTH="11%" HEIGHT="50">
<center>Very
<br>Accurate
<br><input TYPE="RADIO" NAME="Q1" VALUE="5"></center>
</td>
</tr>

<tr>
<td VALIGN=TOP WIDTH="5%" HEIGHT="51">2.&nbsp;</td>

<td VALIGN=TOP WIDTH="28%" HEIGHT="51">Make friends easily.</td>

<td VALIGN=TOP WIDTH="14%" HEIGHT="51">
<center>Very
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q2" VALUE="1"></center>
</td>

<td VALIGN=TOP WIDTH="13%" HEIGHT="51">
<center>Moderately
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q2" VALUE="2"></center>
</td>

<td VALIGN=TOP WIDTH="17%" HEIGHT="51">
<center>Neither Accurate
<br>Nor Inaccurate
<br><input TYPE="RADIO" NAME="Q2" VALUE="3"></center>
</td>

<td VALIGN=TOP WIDTH="12%" HEIGHT="51">
<center>Moderately
<br>Accurate
<br><input TYPE="RADIO" NAME="Q2" VALUE="4"></center>
</td>

<td VALIGN=TOP WIDTH="11%" HEIGHT="51">
<center>Very
<br>Accurate
<br><input TYPE="RADIO" NAME="Q2" VALUE="5"></center>
</td>
</tr>

<tr>
<td VALIGN=TOP WIDTH="5%" HEIGHT="51">3.&nbsp;</td>

<td VALIGN=TOP WIDTH="28%" HEIGHT="51">Have a vivid imagination.</td>

<td VALIGN=TOP WIDTH="14%" HEIGHT="51">
<center>Very
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q3" VALUE="1"></center>
</td>

<td VALIGN=TOP WIDTH="13%" HEIGHT="51">
<center>Moderately
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q3" VALUE="2"></center>
</td>

<td VALIGN=TOP WIDTH="17%" HEIGHT="51">
<center>Neither Accurate
<br>Nor Inaccurate
<br><input TYPE="RADIO" NAME="Q3" VALUE="3"></center>
</td>

<td VALIGN=TOP WIDTH="12%" HEIGHT="51">
<center>Moderately
<br>Accurate
<br><input TYPE="RADIO" NAME="Q3" VALUE="4"></center>
</td>

<td VALIGN=TOP WIDTH="11%" HEIGHT="51">
<center>Very
<br>Accurate
<br><input TYPE="RADIO" NAME="Q3" VALUE="5"></center>
</td>
</tr>

<tr>
<td VALIGN=TOP WIDTH="5%" HEIGHT="51">4.&nbsp;</td>

<td VALIGN=TOP WIDTH="28%" HEIGHT="51">Trust others.</td>

<td VALIGN=TOP WIDTH="14%" HEIGHT="51">
<center>Very
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q4" VALUE="1"></center>
</td>

<td VALIGN=TOP WIDTH="13%" HEIGHT="51">
<center>Moderately
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q4" VALUE="2"></center>
</td>

<td VALIGN=TOP WIDTH="17%" HEIGHT="51">
<center>Neither Accurate
<br>Nor Inaccurate
<br><input TYPE="RADIO" NAME="Q4" VALUE="3"></center>
</td>

<td VALIGN=TOP WIDTH="12%" HEIGHT="51">
<center>Moderately
<br>Accurate
<br><input TYPE="RADIO" NAME="Q4" VALUE="4"></center>
</td>

<td VALIGN=TOP WIDTH="11%" HEIGHT="51">
<center>Very
<br>Accurate
<br><input TYPE="RADIO" NAME="Q4" VALUE="5"></center>
</td>
</tr>

<tr>
<td VALIGN=TOP WIDTH="5%" HEIGHT="51">5.&nbsp;</td>

<td VALIGN=TOP WIDTH="28%" HEIGHT="51">Complete tasks successfully.</td>

<td VALIGN=TOP WIDTH="14%" HEIGHT="51">
<center>Very
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q5" VALUE="1"></center>
</td>

<td VALIGN=TOP WIDTH="13%" HEIGHT="51">
<center>Moderately
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q5" VALUE="2"></center>
</td>

<td VALIGN=TOP WIDTH="17%" HEIGHT="51">
<center>Neither Accurate
<br>Nor Inaccurate
<br><input TYPE="RADIO" NAME="Q5" VALUE="3"></center>
</td>

<td VALIGN=TOP WIDTH="12%" HEIGHT="51">
<center>Moderately
<br>Accurate
<br><input TYPE="RADIO" NAME="Q5" VALUE="4"></center>
</td>

<td VALIGN=TOP WIDTH="11%" HEIGHT="51">
<center>Very
<br>Accurate
<br><input TYPE="RADIO" NAME="Q5" VALUE="5"></center>
</td>
</tr>

<tr>
<td VALIGN=TOP WIDTH="5%" HEIGHT="51">6.&nbsp;</td>

<td VALIGN=TOP WIDTH="28%" HEIGHT="51">Get angry easily.</td>

<td VALIGN=TOP WIDTH="14%" HEIGHT="51">
<center>Very
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q6" VALUE="1"></center>
</td>

<td VALIGN=TOP WIDTH="13%" HEIGHT="51">
<center>Moderately
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q6" VALUE="2"></center>
</td>

<td VALIGN=TOP WIDTH="17%" HEIGHT="51">
<center>Neither Accurate
<br>Nor Inaccurate
<br><input TYPE="RADIO" NAME="Q6" VALUE="3"></center>
</td>

<td VALIGN=TOP WIDTH="12%" HEIGHT="51">
<center>Moderately
<br>Accurate
<br><input TYPE="RADIO" NAME="Q6" VALUE="4"></center>
</td>

<td VALIGN=TOP WIDTH="11%" HEIGHT="51">
<center>Very
<br>Accurate
<br><input TYPE="RADIO" NAME="Q6" VALUE="5"></center>
</td>
</tr>

<tr>
<td VALIGN=TOP WIDTH="5%" HEIGHT="51">7.&nbsp;</td>

<td VALIGN=TOP WIDTH="28%" HEIGHT="51">Love large parties.</td>

<td VALIGN=TOP WIDTH="14%" HEIGHT="51">
<center>Very
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q7" VALUE="1"></center>
</td>

<td VALIGN=TOP WIDTH="13%" HEIGHT="51">
<center>Moderately
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q7" VALUE="2"></center>
</td>

<td VALIGN=TOP WIDTH="17%" HEIGHT="51">
<center>Neither Accurate
<br>Nor Inaccurate
<br><input TYPE="RADIO" NAME="Q7" VALUE="3"></center>
</td>

<td VALIGN=TOP WIDTH="12%" HEIGHT="51">
<center>Moderately
<br>Accurate
<br><input TYPE="RADIO" NAME="Q7" VALUE="4"></center>
</td>

<td VALIGN=TOP WIDTH="11%" HEIGHT="51">
<center>Very
<br>Accurate
<br><input TYPE="RADIO" NAME="Q7" VALUE="5"></center>
</td>
</tr>

<tr>
<td VALIGN=TOP WIDTH="5%" HEIGHT="51">8.&nbsp;</td>

<td VALIGN=TOP WIDTH="28%" HEIGHT="51">Believe in the importance of art.</td>

<td VALIGN=TOP WIDTH="14%" HEIGHT="51">
<center>Very
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q8" VALUE="1"></center>
</td>

<td VALIGN=TOP WIDTH="13%" HEIGHT="51">
<center>Moderately
<br>Inaccurate
<br><input TYPE="RADIO" NAME="Q8" VALUE="2"></center>
</td>

<td VALIGN=TOP WIDTH="17%" HEIGHT="51">
<center>Neither Accurate
<br>Nor Inaccurate
<br><input TYPE="RADIO" NAME="Q8" VALUE="3"></center>
</td>

<td VALIGN=TOP WIDTH="12%" HEIGHT="51">
<center>Moderately
<br>Accurate
<br><input TYPE="RADIO" NAME="Q8" VALUE="4"></center>
</td>

<td VALIGN=TOP WIDTH="11%" HEIGHT="51">
<center>Very
<br>Accurate
<br><input TYPE="RADIO" NAME="Q8" VALUE="5"></center>
</td>
</tr>

<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>9.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Use others for my own ends.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q9" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q9" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q9" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q9" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q9" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>10.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Like to tidy up.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q10" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q10" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q10" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q10" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q10" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>11.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Often feel blue.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q11" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q11" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q11" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q11" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q11" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>12.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Take charge.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q12" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q12" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q12" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q12" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q12" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>13.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Experience my emotions intensely.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q13" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q13" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q13" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q13" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q13" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>14.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Love to help others.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q14" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q14" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q14" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q14" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q14" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>15.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Keep my promises.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q15" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q15" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q15" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q15" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q15" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>16.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Find it difficult to approach others.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q16" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q16" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q16" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q16" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q16" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>17.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am always busy.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q17" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q17" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q17" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q17" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q17" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>18.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Prefer variety to routine.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q18" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q18" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q18" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q18" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q18" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>19.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Love a good fight.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q19" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q19" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q19" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q19" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q19" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>20.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Work hard.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q20" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q20" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q20" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q20" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q20" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>21.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Go on binges.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q21" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q21" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q21" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q21" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q21" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>22.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Love excitement.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q22" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q22" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q22" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q22" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q22" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>23.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Love to read challenging material.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q23" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q23" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q23" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q23" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q23" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>24.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Believe that I am better than others.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q24" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q24" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q24" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q24" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q24" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>25.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am always prepared.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q25" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q25" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q25" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q25" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q25" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>26.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Panic easily.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q26" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q26" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q26" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q26" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q26" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>27.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Radiate joy.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q27" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q27" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q27" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q27" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q27" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>28.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Tend to vote for liberal political candidates.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q28" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q28" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q28" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q28" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q28" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>29.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Sympathize with the homeless.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q29" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q29" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q29" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q29" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q29" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>30.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Jump into things without thinking.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q30" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q30" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q30" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q30" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q30" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>31.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Fear for the worst.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q31" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q31" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q31" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q31" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q31" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>32.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Feel comfortable around people.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q32" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q32" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q32" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q32" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q32" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>33.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Enjoy wild flights of fantasy.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q33" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q33" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q33" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q33" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q33" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>34.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Believe that others have good intentions.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q34" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q34" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q34" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q34" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q34" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>35.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Excel in what I do.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q35" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q35" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q35" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q35" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q35" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>36.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Get irritated easily.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q36" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q36" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q36" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q36" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q36" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>37.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Talk to a lot of different people at parties.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q37" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q37" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q37" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q37" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q37" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>38.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>See beauty in things that others might not notice.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q38" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q38" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q38" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q38" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q38" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>39.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Cheat to get ahead.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q39" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q39" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q39" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q39" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q39" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>40.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Often forget to put things back in their proper place.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q40" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q40" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q40" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q40" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q40" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>41.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Dislike myself.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q41" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q41" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q41" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q41" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q41" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>42.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Try to lead others.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q42" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q42" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q42" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q42" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q42" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>43.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Feel others' emotions.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q43" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q43" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q43" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q43" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q43" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>44.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am concerned about others.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q44" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q44" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q44" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q44" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q44" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>45.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Tell the truth.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q45" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q45" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q45" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q45" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q45" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>46.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am afraid to draw attention to myself.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q46" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q46" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q46" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q46" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q46" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>47.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Am always on the go.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q47" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q47" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q47" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q47" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q47" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>48.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Prefer to stick with things that I know.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q48" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q48" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q48" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q48" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q48" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>49.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Yell at people.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q49" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q49" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q49" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q49" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q49" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>50.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Do more than what's expected of me.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q50" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q50" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q50" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q50" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q50" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>51.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Rarely overindulge.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q51" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q51" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q51" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q51" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q51" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>52.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Seek adventure.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q52" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q52" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q52" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q52" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q52" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>53.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Avoid philosophical discussions.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q53" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q53" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q53" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q53" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q53" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>54.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Think highly of myself.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q54" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q54" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q54" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q54" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q54" VALUE="1">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>55.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Carry out my plans.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q55" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q55" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q55" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q55" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q55" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>56.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Become overwhelmed by events.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q56" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q56" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q56" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q56" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q56" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>57.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Have a lot of fun.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q57" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q57" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q57" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q57" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q57" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>58.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Believe that there is no absolute right or wrong.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q58" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q58" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q58" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q58" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q58" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>59.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Feel sympathy for those who are worse off than myself.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q59" VALUE="1">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q59" VALUE="2">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q59" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q59" VALUE="4">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q59" VALUE="5">
</center></td>
</TR>
<TR><TD WIDTH="5%" VALIGN="TOP" HEIGHT=51>
<P>60.&nbsp;</TD>
<TD WIDTH="28%" VALIGN="TOP" HEIGHT=51>
<P>Make rash decisions.</TD>
<TD WIDTH="14%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q60" VALUE="5">
</center></td>
<TD WIDTH="13%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q60" VALUE="4">
</center></td>
<TD WIDTH="17%" VALIGN="TOP" HEIGHT=51>
<center>Neither Accurate <BR>
Nor Inaccurate <BR>

<INPUT TYPE="RADIO" NAME="Q60" VALUE="3">
</center></td>
<TD WIDTH="12%" VALIGN="TOP" HEIGHT=51>
<center>Moderately <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q60" VALUE="2">
</center></td>
<TD WIDTH="11%" VALIGN="TOP" HEIGHT=51>
<center>Very <BR>
Accurate <BR>

<INPUT TYPE="RADIO" NAME="Q60" VALUE="1">
</center></td>
</TR>
</TABLE>


<p><input TYPE="submit"  VALUE="Send " name="submit"><b>&nbsp; This will send your answers
to be scored and take you to the next 60 questions.</b></form>
</div>
ENDOFTEXT
print $query->end_html;