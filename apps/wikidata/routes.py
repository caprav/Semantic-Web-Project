"""
Author: Sharayu
Created a new route file to handle grammy award logic 

"""
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
import sys
from apps import db, login_manager
from apps.wikidata import blueprint
from  apps.wikidata.insert_artist import select_all_artists,create_connection
import requests
from SPARQLWrapper import SPARQLWrapper, JSON

 

from flask import jsonify 

import sqlite3
from sqlite3 import Error
import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
database = os.path.join(basedir, 'db.sqlite3')
 
qid_dict = {
'Vladimir Horowitz': 'Q192506',
'Beyonce': 'Q36153',
'Aretha Franklin': 'Q125121',
'Bob Dylan': 'Q392',
'Adele': 'Q23215',
'David Foster': 'Q77112',
'Michael Jackson': 'Q2831',
'Glen Campbell': 'Q162667',
'Count Basie': 'Q107008',
'Taylor Swift': 'Q26876',
'John Mayer': 'Q215215',
'Rihanna': 'Q36844',
'Herbie Hancock': 'Q105875',
'Joni Mitchell': 'Q205721',
'Kendrick Lamar': 'Q130798',
'Tony Bennett': 'Q296729',
'Daniel Lanois': 'Q935369',
'Billie Eilish': 'Q29564107',
'James Mallinson': 'Q6138848',
'James Horner': 'Q106221',
'Alanis Morissette': 'Q130742',
'Tina Turner': 'Q131814',
'Henry Mancini': 'Q185928',
'Seal': 'Q218091',
'Clive Davis': 'Q1101938',
'Igor Stravinsky': 'Q7314',
'Frank Sinatra': 'Q40912',
'Lady Gaga': 'Q19848',
'Alan Menken': 'Q317272',
'Mariah Carey': 'Q41076',
'Willie Nelson': 'Q206112',
'Christina Aguilera': 'Q41594',
'Olivia Newton-John': 'Q185165',
'Rob Thomas': 'Q754094',
'Sam Smith': 'Q15123969',
'Humberto Gatica': 'Q16729211',
'Judy Garland': 'Q11637',
'Oscar Peterson': 'Q105349',
'John Prine': 'Q520296',
'Phil Ramone': 'Q204323',
'Johnny Mercer': 'Q363698',
'Madonna': 'Q1744',
'André Previn': 'Q155712',
'The-Dream': 'Q351055',
'Kelly Clarkson': 'Q483507',
'Dolly Parton': 'Q180453',
'Jay-Z': 'Q62766',
'Peter Gabriel': 'Q175195',
'Shania Twain': 'Q131433',
'Jacob Collier': 'Q24900882',
'Maya Angelou': 'Q19526',
'Leonard Cohen': 'Q1276',
'Pink': 'Q160009',
'Quincy Jones': 'Q193645',
'Domenico Modugno': 'Q201392',
'Bobby McFerrin': 'Q310894',
'Bobby Darin': 'Q311267',
'Giorgio Moroder': 'Q312674',
'Al Green': 'Q313260',
'Paul Epworth': 'Q515883',
'Norah Jones': 'Q549981',
'Mark Linett': 'Q6768604',
'Duke Ellington': 'Q4030',
'Charlie Parker': 'Q103767',
'Ravi Shankar': 'Q103774',
'Doris Day': 'Q104372',
'Lena Horne': 'Q112307',
'Itzhak Perlman': 'Q215905',
'Glenn Gould': 'Q216924',
'Loretta Lynn': 'Q272931',
'George Solti': 'Q128085',
'George Martin': 'Q191819',
'Carole King': 'Q217787',
'Marilyn Bergman': 'Q442879',
'Alan Bergman': 'Q1857066',
'Ed Sheeran': 'Q47447',
'Alicia Keys': 'Q121507',
'Sting': 'Q483203',
'Bobby Russell': 'Q3641411',
'Thelonious Monk': 'Q109612',
'Sarah McLachlan': 'Q224650',
'Peggy Lee': 'Q229139',
'Linda Ronstadt': 'Q229375',
'Billie Holiday': 'Q104358',
'Charles Mingus': 'Q107432',
'Art Tatum': 'Q109053',
'Kris Kristofferson': 'Q208681',
'Burt Bacharach': 'Q212762',
'Clifton Chenier': 'Q1101377',
'Skrillex': 'Q19004',
'Kelly Rowland': 'Q184249',
'Common': 'Q286022',
'Frank Ocean': 'Q357645',
'Jay Graydon': 'Q1145989',
'Thundercat': 'Q15285290',
'Pharrell Williams': 'Q14313',
'Lizzo': 'Q16232225',
'Hildur Gu ': 'Q433734',
'Chips Moman': 'Q1074626',
'Alan Broadbent': 'Q1145788',
'David Houston': 'Q1174771',
'Kacey Musgraves': 'Q2783855',
'Jimmie Haskell': 'Q3178999',
'Barack Obama': 'Q76',
'Kenny Rogers': 'Q217160',
'Randy Travis': 'Q467519',
'Ken Burns': 'Q616886',
'Neil Young': 'Q633',
'Beck': 'Q11901',
'Stan Getz': 'Q30587',
'Yoko Ono': 'Q117012',
'João Gilberto': 'Q192359',
'Billy Joel': 'Q194333',
'Hayley Williams': 'Q201562',
'Astrud Gilberto': 'Q230401',
'Trevor Horn': 'Q313092',
'Guy-Manuel de Homem-Christo': 'Q471650',
'Lyle Lovett': 'Q543637',
'Taylor York': 'Q678041',
'Dave Pirner': 'Q1173317',
'Hans Graf': 'Q1979804',
'Tom Elmhirst': 'Q7815719',
'Mike Bozzi': 'Q18149600',
'Mark Rankin': 'Q18352852',
'Jahaan Sweet': 'Q113584842',
'John Lennon': 'Q1203',
'Janis Joplin': 'Q1514',
'Ella Fitzgerald': 'Q1768',
'Louis Armstrong': 'Q1779',
'Paul Simon': 'Q4028',
'James Brown': 'Q5950',
'Arturo Toscanini': 'Q13003',
'Freddie Mercury': 'Q15869',
'Diana Ross': 'Q36290',
'Johnny Cash': 'Q42775',
'Little Richard': 'Q82222',
'Miles Davis': 'Q93341',
'Dave Brubeck': 'Q108597',
'Julie Andrews': 'Q161819',
'Enrico Caruso': 'Q170726',
'Max Roach': 'Q175899',
'B.B. King': 'Q188969',
'Bo Diddley': 'Q208881',
'Harry Belafonte': 'Q214959',
'Dean Martin': 'Q215359',
'John Entwistle': 'Q215835',
'Otis Redding': 'Q217839',
'Sarah Vaughan': 'Q229513',
'Leontyne Price': 'Q233718',
'Kitty Wells': 'Q272913',
'Cab Calloway': 'Q273079',
'Sammy Davis Jr.': 'Q297816',
'Curtis Mayfield': 'Q310170',
'Art Blakey': 'Q311715',
'George Clinton': 'Q336272',
'Gene Autry': 'Q342723',
'Benny Carter': 'Q356715',
'Hank Jones': 'Q447907',
'Johnny Mathis': 'Q449612',
'Pinetop Perkins': 'Q458229',
'Rosemary Clooney': 'Q466508',
'Celia Cruz': 'Q474045',
'George Jones': 'Q508202',
'Bobby Bland': 'Q541634',
'Ray Charles': 'Q544387',
'Billy Eckstine': 'Q545464',
'David Edwards': 'Q560354',
'Sly Stone': 'Q713829',
'George Beverly Shea': 'Q888118',
'Morton Gould': 'Q1352656',
'Armando Manzanero': 'Q1453045',
'Maud Powell': 'Q1772440',
'Ella Jenkins': 'Q3051334',
'Walt Disney': 'Q8704',
'Thomas Edison': 'Q8743',
'Ennio Morricone': 'Q23848',
'Gerry Goffin': 'Q48774',
'Ira Gershwin': 'Q61059',
'Emile Berliner': 'Q71004',
'George Gershwin': 'Q123829',
'Milt Gabler': 'Q145823',
'Krzysztof Penderecki': 'Q153469',
'Stephen Sondheim': 'Q153579',
'Aaron Copland': 'Q192185',
'Robert Moog': 'Q200883',
'Phil Spector': 'Q213793',
'Cole Porter': 'Q215120',
'Les Paul': 'Q262399',
'Richard Rodgers': 'Q269094',
'Marian McPartland': 'Q275616',
'Leopold Stokowski': 'Q297562',
'Jerome Kern': 'Q313270',
'Elliott Carter': 'Q318835',
'Oscar Hammerstein II': 'Q319693',
'Sam Phillips': 'Q321354',
'Herb Alpert': 'Q344822',
'Orrin Keepnews': 'Q352028',
'Ahmet Ertege': 'Q352760',
'W. C. Handy': 'Q352967',
'Berry Gordy': 'Q355288',
'Dick Clark': 'Q366563',
'Eldridge R. Johnson': 'Q370171',
'Billy Strayhorn': 'Q380626',
'Pierre Cossette': 'Q446753',
'Hal David': 'Q449030',
'Alan Freed': 'Q453956',
'Phil Chess': 'Q456295',
'Hoagy Carmichael': 'Q460662',
'Rosanne Cash': 'Q462289',
'Willie Mitchell': 'Q465105',
'Estelle Axton': 'Q535907',
'Jerry Wexler': 'Q537722',
'Frederick Loewe': 'Q551678',
'Thomas A. Dorsey': 'Q562158',
'Arif Mardin': 'Q660545',
'Nasuhi Ertegün': 'Q710748',
'Billy Taylor': 'Q718617',
'Lorenz Hart': 'Q725828',
'Jerry Moss': 'Q744190',
'Bruce Lundvall': 'Q776922',
'Chris Blackwell': 'Q861129',
'Dave Bartholomew': 'Q920288',
'Rudy Van Gelder': 'Q945681',
'Alan Jay Lerner': 'Q961893',
'Cosimo Matassa': 'Q1136060',
'Tom Dowd': 'Q1341906',
'George Avakian': 'Q1382368',
'George T. Simon': 'Q1508326',
'Paul Weston': 'Q1765101',
'Leonard Chess': 'Q1818980',
'Owen Bradley': 'Q2042598',
'Jac Holzman': 'Q2079102',
'Jim Marshall': 'Q2660967',
'Alan W. Livingston': 'Q3000674',
'Walter C. Miller': 'Q3565708',
'Al Bell': 'Q4703577',
'Al Schmitt': 'Q4704778',
'Chris Albertson': 'Q5105702',
'Florence Greenberg': 'Q5460628',
'Goddard Lieberson': 'Q5576257',
'Harold Bradley': 'Q5660145',
'John Culshaw': 'Q6227849',
'Rick Hall': 'Q7331436',
'Wilma Cozart Fine': 'Q8022655',
'Larry Hiller': 'Q18643476',
'Christine M. Farnon': 'Q18643479',
'Bruno Jackson Mars': 'Q1450',
'Cannonball Adderley': 'Q110477',
'Bonnie Raitt': 'Q234693',
'Harry Nilsson': 'Q281034',
'Tim Rice': 'Q298295',
'Cynthia Weil': 'Q461008',
'Terri Lyne Carrington': 'Q466966',
'Roy Hargrove': 'Q648750',
'Chad Hugo': 'Q706641',
'Johnny Mandel': 'Q975609',
'David Murray': 'Q1175803',
'Leslie Bricusse': 'Q1305608',
'Ludwig Göransson': 'Q1358202',
'Paul Francis Webster': 'Q1620897',
'Larry Klein': 'Q1806079',
'Jimmy Napes': 'Q19119517',
'William Phillips': 'Q19119560',
'Dua Lipa': 'Q21914464',
'H.E.R.': 'Q30639849',
'Olivia Rodrigo': 'Q63243883',
'David Bowie': 'Q5383',
'Chuck Berry': 'Q5921',
'John Coltrane': 'Q7346',
'Lionel Richie': 'Q26695',
'Nelly Furtado': 'Q80424',
'Fred Astaire': 'Q100937',
'Frank Zappa': 'Q127330',
'Jerry Lee Lewis': 'Q202729',
'Stéphane Grappelli': 'Q206244',
'Mahalia Jackson': 'Q206466',
'Pau Casals': 'Q208537',
'Fats Domino': 'Q209586',
'k.d. lang': 'Q230454',
'Anne Murray': 'Q236543',
'Jascha Heifetz': 'Q243472',
'Paul Robeson': 'Q273233',
'Sam Cooke': 'Q295919',
'Smokey Robinson': 'Q310332',
'Fats Waller': 'Q310476',
'Ryan Tedder': 'Q351061',
'Lightnin Hopkins': 'Q435552',
'Christopher Cross': 'Q445438',
'Louis Jordan': 'Q461011',
'Thomas Bangalter': 'Q471656',
'Donny Hathaway': 'Q507864',
'Dan Hill': 'Q1159082',
'David Cole': 'Q1174042',
'Michael Omartian': 'Q1645182',
'Supriyo Bandyopadhyay': 'Q90565644',
'Arthur Lewis Costa': 'Q105475057',
'Elvis Presley': 'Q303',
'Bob Marley': 'Q409',
'Stevie Wonder': 'Q714',
'Paul McCartney': 'Q2599',
'Woody Guthrie': 'Q4061',
'Barbra Streisand': 'Q4636',
'Jimi Hendrix': 'Q5928',
'Buddy Holly': 'Q5977',
'Selena': 'Q23543',
'John Lee Hooker': 'Q44570',
'Benny Goodman': 'Q46755',
'Eric Clapton': 'Q48187',
'Dizzy Gillespie': 'Q49575',
'Chet Atkins': 'Q72096',
'Bing Crosby': 'Q72984',
'Earl Scruggs': 'Q74032',
'Bessie Smith': 'Q93349',
'Glenn Miller': 'Q103651',
'Julio Iglesias': 'Q122003',
'Maria Callas': 'Q128297',
'Irving Berlin': 'Q128746',
'Joan Baez': 'Q131725',
'Nat King Cole': 'Q137042',
'Leonard Bernstein': 'Q152505',
'Bill Monroe': 'Q170042',
'Patti Page': 'Q175759',
'Etta James': 'Q182725',
'Merle Haggard': 'Q183092',
'Arthur Rubinstein': 'Q183182',
'Roy Orbison': 'Q188426',
'Marvin Gaye': 'Q189758',
'Robert Johnson': 'Q192133',
'Andrés Segovia Torres': 'Q192529',
'Antônio Carlos Jobim': 'Q200131',
'Hank Williams': 'Q206181',
'Bill Evans': 'Q208205',
'Ornette Coleman': 'Q208797',
'Muddy Waters': 'Q220707',
'Brenda Lee': 'Q230925',
'Roberta Flack': 'Q231484',
'Marian Anderson': 'Q231923',
'Jessye Norman': 'Q240937',
'Pete Seeger': 'Q244441',
'Patsy Cline': 'Q273080',
'Richard Pryor': 'Q294912',
'Sonny Rollins': 'Q299208',
'Isaac Stern': 'Q311317',
'Tito Puente': 'Q317122',
'Jelly Roll Morton': 'Q317128',
'Charlie Haden': 'Q319283',
'Artie Shaw': 'Q320065',
'Perry Como': 'Q333405',
'Woody Herman': 'Q349357',
'Van Cliburn': 'Q366355',
'Gil Scott-Heron': 'Q378858',
'Ahmad Jamal': 'Q379613',
'Clark Terry': 'Q432924',
'Roy Haynes': 'Q448235',
'Roy Acuff': 'Q455773',
'Doc Watson': 'Q465636',
'Mel Tormé': 'Q470848',
'Mitch Miller': 'Q709499',
'Bob Wills': 'Q888326',
'Tom Paxton': 'Q1351527',
'Eminem': 'Q5608',
'Kanye West': 'Q15935',
'Drake': 'Q33240',
'Justin Timberlake': 'Q43432',
'Meshell Ndegeocello': 'Q72720',
'James Fauntleroy II': 'Q152330',
'Meat Loaf': 'Q152929',
'Usher': 'Q165911',
'Timbaland': 'Q179257',
'Fergie': 'Q180004',
'Ludacris': 'Q193676',
'T.I.': 'Q214227',
'Nelly': 'Q218992',
'Aphex Twin': 'Q223161',
'Estelle': 'Q230622',
'Irene Cara': 'Q234169',
'Eve': 'Q239464',
'R. Kelly': 'Q273055',
'Kid Cudi': 'Q299138',
'Nancy Wilson': 'Q467690',
'Gwen Stefani': 'Q483379',
'Diplo': 'Q533781',
'Betty Wright': 'Q547181',
'Bilal': 'Q860283',
'Cecil McBee': 'Q1052331',
'Reggie Lucas': 'Q1130554',
'Raphael Saadiq': 'Q1337779',
'Jerome Harmon': 'Q6182726',
'Detail': 'Q15059449',
'Dre Moon': 'Q17279693',
'Rasool Diaz': 'Q19120110',
'Brian Soko': 'Q19120159',
'Jimmy Jam': 'Q20202184',
'Terry Lewis': 'Q20202280',
'Shakira': 'Q34424',
'David Zinman': 'Q115696',
'Lorin Maazel': 'Q117710',
'Jamie Foxx': 'Q171905',
'Ike Turner': 'Q208871',
'Nino Rota': 'Q214665',
'Monica': 'Q231487',
'Patti LuPone': 'Q270324',
'Riccardo Muti': 'Q276038',
'Anthony Hamilton': 'Q573323',
'László Polgár': 'Q687205',
'Brandy': 'Q690974',
'Donna Summer': 'Q908933',
'Tony Kaye': 'Q1070690',
'Gary Clark Jr.': 'Q1153310',
'Malcolm-Jamal Warner': 'Q1349215',
'Robert Glasper': 'Q1370642',
'Gerald Levert': 'Q1383872',
'Mathew Cullen': 'Q6787005',
'Valerie Faris': 'Q13644887',
'Lil Nas X': 'Q62591281',
'Calmatic': 'Q106337645',
'"Weird Al" Yankovic': 'Q8349',
'Hans Zimmer': 'Q76364',
'Maurice Jarre': 'Q105487',
'Lebo M.': 'Q109045',
'John Barry': 'Q111074',
'John Williams': 'Q131285',
'Howard Shore': 'Q207773',
'James Newton Howard': 'Q213869',
'Miranda Lambert': 'Q231233',
'Trent Reznor': 'Q282722',
'Alexandre Desplat': 'Q313362',
'Burl Ives': 'Q315723',
'Thomas Newman': 'Q319996',
'David Arnold': 'Q346285',
'Shel Silverstein': 'Q361257',
'Harold Faltermeyer': 'Q372489',
'Paul Buckmaster': 'Q374682',
'Alan Jackson': 'Q380927',
'Nanci Griffith': 'Q447032',
'Rob McConnell': 'Q448257',
'Dave Grusin': 'Q502923',
'Atticus Ross': 'Q520346',
'Steve Goodman': 'Q585159',
'Billy Childs': 'Q863047',
'Byron Gallimore': 'Q1018603',
'Christopher Tin': 'Q1087016',
'Gordon Jenkins': 'Q1388198',
'John Addison': 'Q1699098',
'Kenny ODell': 'Q6021372',
'Julian Raymond': 'Q19159150',
'Nan Schwartz': 'Q91109222',
'Hillary Clinton': 'Q6294',
'Michelle Obama': 'Q13133',
'Henry Fonda': 'Q19155',
'Steve Jobs': 'Q19837',
'Will Smith': 'Q40096',
'Charles Laughton': 'Q55264',
'Alfred Lion': 'Q68260',
'Béla Bartók': 'Q83326',
'Sidney Poitier': 'Q104049',
'Richard Harris': 'Q106775',
'Magic Johnson': 'Q134183',
'Ben Kingsley': 'Q173158',
'Christopher Reeve': 'Q174311',
'Garrison Keillor': 'Q183031',
'John Gielgud': 'Q204685',
'Stephen Colbert': 'Q212886',
'Helen Hayes': 'Q213302',
'Garth Brooks': 'Q216288',
'Edward Albee': 'Q219420',
'Viola Davis': 'Q229181',
'Janis Ian': 'Q235515',
'Julie Harris': 'Q236708',
'Kitarō': 'Q273652',
'LeVar Burton': 'Q312570',
'George Burns': 'Q344793',
'Betty White': 'Q373895',
'Michael J. Fox': 'Q395274',
'Harold Arlen': 'Q448644',
'Andreas Vollenweider': 'Q458828',
'Ossie Davis': 'Q515632',
'John Hammond': 'Q549141',
'Alan Lomax': 'Q558104',
'Charlie Rich': 'Q563057',
'Allen Toussaint': 'Q963044',
'Young MC': 'Q1132431',
'Dave Alvin': 'Q1173086',
'Don Cornelius': 'Q1239072',
'Norman Granz': 'Q1382555',
'Gregg Karukas': 'Q1498190',
'Ryan Lewis': 'Q1972952',
'The Weeknd': 'Q2121062',
'Omar Akram': 'Q3882068',
'Wanz': 'Q7031879',
'Chance the Rapper': 'Q12470060',
'Frances Preston': 'Q18643480',
'Robert Bialek': 'Q84761069',
'Red Hot Chili Peppers' : 'Q10708'
,'George Solti':'None'
,'Quincy Jones':'Q25190073'
,'Chick Corea':'Q5191353'
,'Alison Krauss':'Q371782'
,'Stevie Wonder':'Q714'
,'John Williams':'Q131285'
,'Vladimir Horowitz':'Q192506'
,'Jay-Z':'Q62766'
,'Kanye West':'Q2271213'
,'Vince Gill':'Q924232'
,'Henry Mancini':'Q185928'
,'Bruce Springsteen':'Q1225'
,'Pat Metheny':'Q213887'
,'Al Schmitt':'Q4704778'
,'Tony Bennett':'Q296729'
,'Yo-Yo Ma':'Q234891'
,'Aretha Franklin':'Q125121'
,'Jimmy Sturr':'Q4442402'
,'Kendrick Lamar':'Q130798'
,'Ray Charles':'Q544387'
,'Leonard Bernstein':'Q152505'
,'James Mallinson':'Q25189544'
,'Robert Shaw':'Q492138'
,'Paul Simon':'Q4028'
,'Steven Epstein':'Q669283'
,'Kirk Franklin':'Q1349627'
,'David Frost':'Q5233879'
,'Eminem':'Q5608'
,'Bruno Mars':'Q1450'
,'Foo Fighters':'Q483718'
,'CeCe Winans':'Q538696'
,'Alicia Keys':'Q121507'
,'Adele':'Q23215'
,'Bela Fleck':'Q561390'
,'Jerry Douglas':'Q2667430'
,'Phil Ramone':'Q204323'
,'Alison Krauss and Union Station':'Q10853874'
,'Jay David Saks':'None'
,'Emmylou Harris':'Q231286'
,'Michael Jackson':'Q2831'
,'Pharrell Williams':'Q14313'
,'Lady Gaga':'Q19848'
,'Johnny Cash':'Q107463189'
,'Bonnie Raitt':'Q234693'
,'Robert Woods':'Q1265326'
,'Taylor Hawkins':'Q312395'
,'Leontyne Price':'Q233718'
,'Ella Fitzgerald':'Q1768'
,'T Bone Burnett':'Q1225141'
,'Thomas Z Shepard':'None'
,'John Legend':'Q44857'
,'The Chicks':'Q29860404'
,'Jay Newland':'Q6166974'
,'Babyface':'Q4838472'
,'Taylor Swift':'Q26876'
,'Michael Tilson Thomas':'Q520493'
,'Shirley Caesar':'Q7498714'
,'Al Green':'Q14469655'
,'Arif Mardin':'Q660545'
,'Roger Miller':'Q7358650'
,'Andre Previn':'Q155712'
,'Justin Timberlake':'Q43432'
,'Bob Dylan':'Q392'
,'James Levine':'Q27107622'
,'Linda Ronstadt':'Q6551931'
,'Chaka Khan':'Q229498'
,'Bobby McFerrin':'Q310894'
,'Carlos Santana':'Q5042623'
,'Pat Metheny Group':'Q985460'
,'Willie Nelson':'Q8021739'
,'Mary J. Blige':'Q228909'
,'Rihanna':'Q36844'
,'Frank Sinatra':'Q40912'
,'Sheryl Crow':'Q1932542'
,'James Blackwood Sr.':'None'
,'Brandi Carlile':'Q3283299'
,'Natalie Cole':'Q231942'
,'Count Basie':'Q107008'
,'Joni Mitchell':'Q2256372'
,'Norah Jones':'Q549981'
,'Hillary Scott':'Q232687'
,'Emerson String Quartet':'Q681006'
,'Dolly Parton':'Q1749197'
,'Barbra Streisand':'Q4636'
,'Luther Vandross':'Q311306'
,'Asleep At The Wheel':'None'
,'Tina Turner':'Q100949053'
,'Usher':'Q165911'
,'Fergie':'Q5444141'
,'Take 6':'Q327344'
,'Lauryn Hill':'Q214226'
,'Blackwood Brothers':'Q19919668'
,'Anita Baker':'Q255697'
,'Metallica':'Q6822842'
,'Rick Rubin':'Q587361'
,'James Blackwood Jr.':'None'
,'Chris Stapleton':'Q5108148'
,'Carrie Underwood':'Q215546'
,'Ziggy Marley':'Q25096774'
,'Eddie Palmieri':'Q1282931'
,'The Manhattan Transfer':'Q3988222'
,'Art Garfunkel':'Q4039'
,'Anderson .Paak':'Q20810369'
,'Skrillex':'Q19004'
,'Santana':'Q873384'
,'Stephen Marley':'Q468677'
,'Finneas OConnell':'Q20029978'
,'Prince':'Q7542'
,'Madonna':'Q112659641'
,'will.i.am':'Q185610'
,'Dr. Dre':'Q6078'
,'André 3000':'Q448837'
,'Gladys Knight':'Q235952'
,'Thomas Frost':'Q21071867'
,'John Mayer':'Q215215'
,'Billie Eilish':'Q29564107'
,'Los Tigres del Norte':'Q1467310'
,'Toni Braxton':'Q1059395'
,'Simon & Garfunkel':'Q484918'
,'Ricky Skaggs and Kentucky Thunder':'Q6392405'
,'Leslie Ann Jones':'Q6530602'
,'Whitney Houston':'Q34389'
,'Robert M. Jones':'None'
,'Amy Grant':'Q464213'
,'James Taylor':'Q113493060'
,'Eagles':'Q113961760'
,'Big Boi':'Q371202'
,'Jack Antonoff':'Q151304'
,'Questlove':'Q263024'
,'Israel Houghton':'Q5814434'
,'OutKast':'Q472595'
,'Black Eyed Peas':'Q134541'
,'Dr. John':'Q511074'
,'Tito Puente':'Q317122'
,'Tim Martyn':'None'
,'Kacey Musgraves':'Q2783855'
,'Mariah Carey':'Q41076'
,'Lil Wayne':'Q15615'
,'Janet Jackson':'Q131324'
,'H.E.R.':'Q30639849'
,'Billy Joel':'Q194333'
,'Christina Aguilera':'Q10747732'
,'Donna Summer':'Q908933'
,'Cee Lo Green':'Q4042'
,'Mary Chapin Carpenter':'Q270765'
,'Peter, Paul & Mary':'Q654716'
,'Dionne Warwick':'Q234695'
,'Michael McDonald':'Q99504025'
,'Sandi Patty':'Q2745548'
,'Kuk Harrell':'Q1653721'
,'Maria Schneider':'Q435179'
,'Childish Gambino':'Q1239933'
,'Robert Glasper':'Q1370642'
,'Jon Batiste':'Q6272528'
,'Lady A':'Q96248034'
,'Christopher Cross':'Q1086616'
,'Missy Elliott':'Q155079'
,'David Russell':'Q5239308'
,'Flaco Jimenez':'Q5456591'
,'Ward Swingle':'Q2549075'
,'India.arie':'None'
,'Timbaland':'Q179257'
,'Erykah Badu':'Q223875'
,'Keith Urban':'Q1951455'
,'PJ Morton':'Q5354186'
,'Lyle Lovett':'Q543637'
,'Lizzo':'Q16232225'
,'Yolanda Adams':'Q270869'
,'Tracy Chapman':'Q129804'
,'The Weeknd':'Q2121062'
,'Marvin Hamlisch':'Q337206'
,'Lisa Lopes':'Q233541'
,'Lenny Kravitz':'Q180224'
,'Carole King':'Q217787'
,'Sade':'Q3461110'
,'Robert Spano':'Q4430666'
,'Will Smith':'Q108861845'
,'Pepe Aguilar':'Q7166214'
,'Silk Sonic':'Q105813956'
,'R. Kelly':'Q273055'
,'Pink':'Q49294'
,'Ludacris':'Q193676'
,'T.I':'None'
,'Gwen Stefani':'Q483379'
,'Loretta Lynn':'Q5137747'
,'Etta James':'Q5404963'
,'Bill Holman':'Q348471'
,'Reba McEntire':'Q7301589'
,'Kelly Clarkson':'Q483507'
,'Elvis Presley':'Q303'
,'Harry Connick Jr.':'Q313755'
,'Destinys Child':'Q153056'
,'The Roots':'Q1052139'
,'Clare Fischer':'Q729139'
,'Puff Daddy':'Q216936'
,'Maroon 5':'Q182223'
,'Maxwell':'Q9095'
,'Diplo':'Q533781'
,'Gloria Estefan':'Q184697'
,'Red Hot Chili Peppers':'Q10708'
,'Los Lobos':'Q87772231'
,'Vikki Carr':'Q301864'
,'Fiona Apple':'Q228968'
,'Lori McKenna':'Q6681105'
,'Rob Thomas':'Q723021'
,'Shawn Colvin':'Q267438'
,'Taj Mahal':'Q9141'
,'Steely Dan':'Q852435'
,'Harry Styles':'Q3626966'
,'James Brown':'Q5950'
,'Chance the Rapper':'Q12470060'
,'Ross Bagdasarian Sr.':'Q1176607'
,'The Carpenters':'Q223495'
,'Olivia Rodrigo':'Q63243883'
,'The Flaming Lips':'Q523184'
,'Megan Thee Stallion':'Q59268408'
,'Lin-Manuel Miranda':'Q1646482'
,'Bob Newhart':'Q718078'
,'Esperanza Spalding':'Q238705'
,'Toto':'Q36709'
,'St. Vincent':'Q16899642'
,'Tool':'Q184827'
,'Lenny White':'Q1818166'
,'Dan + Shay':'Q16959408'
,'Pentatonix':'Q3374926'
,'Jazmine Sullivan':'Q267070'
,'Cyndi Lauper':'Q1545'
,'Melissa Etheridge':'Q10328410'
,'Ariana Grande':'Q151892'
,'Peter Kater':'Q7175100'
,'Patti LaBelle':'Q2058334'
,'T-Pain':'Q221155'
,'Marvin Gaye':'Q189758'
,'Kenny Loggins':'Q435965'
,'Barry White':'Q213647'
,'Yehudi Menuhin':'Q156814'
,'Intocable':'Q2033206'
,'No Doubt':'Q43259'
,'Jimmy Carter':'Q23685'
,'Brian Wilson':'Q4965651'
,'Marc Anthony':'Q6755356'
,'Peter Nero':'Q7176071'
,'Nate Ruess':'Q2760347'
,'Bon Iver':'Q357340'
,'Soundgarden':'Q174817'
,'La Mafia':'Q6463596'
,'LeAnn Rimes':'Q17088795'
,'Brave Combo':'Q2924131'
,'Fleetwood Mac':'Q2398078'
,'Frank Ocean':'Q261436'
,'Jennifer Hudson':'Q192410'
,'Linkin Park':'Q261'
,'Andrew Dost':'Q4756824'
,'Evanescence':'Q5415612'
,'Bad Bunny':'Q44333953'
,'Natalie Hemby':'Q16729754'
,'Nate Hills':'Q179593'
,'Otis Redding':'Q217839'
,'Bobby Darin':'Q19867791'
,'Tyler, the Creator':'Q167635'
,'Vernon Reid':'Q587628'
,'Colbie Caillat':'Q228860'
,'Lorde':'Q112252045'
,'Aaron Dessner':'Q4661964'
,'Ted Nash':'Q7693540'
,'The Wreckers':'Q7776289'
,'Lauren Daigle':'Q18685595'
,'Kaytranada':'Q17153342'
,'Jason Mraz':'Q192515'
,'Nipsey Hussle':'Q2073970'
,'Little Joe y La Familia':'None'
,'Lisa Fischer':'Q536198'
,'Tori Kelly':'Q7825754'
,'Rufus':'Q1186448'
,'Thundercat':'Q7799126'
,'David Robertson':'Q101081860'
,'Selena':'Q23543'
,'Judy Garland':'Q11637'
,'Samara Joy':'Q108311952'
,'Chris Brown':'Q155700'
,'Kenny G':'Q1936095'
,'Doja Cat':'Q51120673'
,'Nas':'Q11789827'
,'SZA':'Q16210722'
,'50 Cent':'Q6386700'
,'Elvis Costello':'Q206939'
,'Ledisi':'Q1811634'
,'Ray Barretto':'Q740099'
,'Miguel':'Q3857242'
,'Pearl Jam':'Q931609'
,'Carter Beauford':'Q964653'
,'Brandy Norwood':'Q690974'
,'Fantasia':'Q192656'
,'Dave Matthews Band':'Q832086'
,'Eddie Blazonczyk':'Q446398'
,'Jon Bon Jovi':'Q150916'
,'J. Cole':'Q204018'
,'Lucky Daye':'Q60687448'
,'DJ Khaled':'Q80805'
,'Q-Tip':'Q42025'
,'Chicago':'Q1297'
,'David Crosby':'Q370560'
,'Cardi B':'Q29033668'
,'The Neptunes':'Q866207'
,'Bon Jovi':'Q13396732'
,'Arcade Fire':'Q1766668'
,'Roddy Ricch':'Q59209423'
,'Ashanti':'Q226930'
,'Al Hirt':'Q658636'
,'Britney Spears':'Q11975'
,'Mariachi Divas':'None'
,'John McLaughlin Williams':'Q6248062'
,'Stephen Stills':'Q914020'
,'Sara Bareilles':'Q230445'
,'Faith Evans':'Q5431183'
,'Lil Baby':'Q50527563'
,'Cher':'Q12003'
,'Queen Latifah':'Q1112005'
,'Mongo Santamaria':'Q472644'
,'Paula Cole':'Q269462'
,'Nat King Cole':'Q137042'
,'Rhonda Vincent':'Q188429'
,'Steve Lacy':'Q104839595'
,'Stargate':'Q11927'
,'Bobby Bare':'Q888450'
,'Crosby, Stills & Nash':'Q733159'
,'Nirvana':'Q111939444'
,'Twenty One Pilots':'Q15958277'
,'Kylie Minogue':'Q11998'
,'Gloria Gaynor':'Q228918'
,'Emilio Navaira':'Q12858184'
,'Ciara':'Q84712796'
,'Fun':'Q360552'
,'Richard Marx':'Q311256'
,'Enrique Iglesias':'Q47122'
,'The Chainsmokers':'Q7721993'
,'Steve Jordan':'Q7612970'
,'Pink Floyd':'Q639863'
,'Michelle Branch':'Q234685'
,'Frank Yankovic':'None'
,'Kentucky Headhunters':'None'
,'Imagine Dragons':'Q6002689'
,'Alfred Newman':'Q4723206'
,'Julieta Venegas':'Q232214'
,'Monica':'Q437778'
,'21 Savage':'Q25095399'
,'Hykeem Carter':'Q70063212'
,'Leon Bridges':'Q60734176'
,'Ella Mai':'Q29033458'
,'Muni Long':'Q7245622'
,'Weezer':'Q209956'
,'Cal Tjader':'Q491368'
,'Mariachi los Camperos':'Q6761738'
,'Texas Tornados':'Q7708180'
,'Los Palominos':'Q6683048'
,'Rüfüs Du Sol':'Q16875193'
,'Meghan Trainor':'Q17403494'
,'La Santa Cecilia':'Q6465167'
,'Lila Downs':'None'
,'The Band Perry':'Q5225933'
,'Lupillo Rivera':'Q547787'
,'Nadia Shpachenko':'None'
,'Andra Day':'Q21004826'
,'Creed':'Q402852'
,'Gloria Cheng':'Q56717105'
,'Bacilos':'Q960323'
,'Los Super Seven':'Q3259771'
,'The Legends':'Q17916924'
,'Paula Abdul':'Q185465'
,'Bobby Brown':'Q4934817'
,'Bo Burnham':'Q887347'
,'Otha Nash':'None'
,'America':'Q30'
,'Lisa Loeb & Nine Stories':'None'
,'Jesse Harris':'Q111962875'
,'Sirah':'Q11739784'
,'Solange':'Q1632886'
,'Chris Perez':'Q2964837'
,'Stephen McLaughlin':'Q7609967'
,'Chente Barrera':'Q19560041'
,'Los Texmaniacs':'Q6683293'
,'Jessica Rivera':'Q13562085'
,'Puff Daddy & The Family':'None'
,'The Product G&B':'Q3988855'
,'Timothy Fallon':'None'
,'Freddie Nartinez Jr.':'None'
,'Daya':'Q5242998'
}


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def process_data(sparql_results):
    awards = []
    image_url = None

    for result in sparql_results["results"]["bindings"]:
        if not image_url:  # Assuming all entries have the same image URL
            image_url = result['image']['value']
        
        award_info = {
            'awardLabel': result['awardLabel']['value'],
            'year': result['year']['value']
        }
        awards.append(award_info)

    return {
        'image': image_url,
        'awards': awards
    }    




@blueprint.route('/search_grammy_artist', methods=['POST'])
def search():
    data = request.get_json()
    user_input = data.get('user_input')

    conn = create_connection()
    suggestions = select_all_artists(conn, user_input)

    

    # Check if suggestions is not empty before appending to the list
    suggestions_list = []

    for suggestion in suggestions:
        # Assuming 'suggestion' is a dictionary representing an object
        suggestions_list.append(suggestion)

    # Return the suggestions list as a JSON response
    return jsonify(suggestions_list)

@blueprint.route('/wikidata_endpoint', methods=['POST'])
def wikidata_endpoint():
    data = request.get_json()
     
    suggestion = data['suggestion'][0]
    suggestion = suggestion.strip("'")

    
    endpoint_url = 'https://query.wikidata.org/sparql'

    # Headers for the SPARQL request
    headers = {
        'Accept': 'application/sparql-results+json'
    }
    suggestion = suggestion.strip("[]").strip("'")

     

   
    sparql_query = """SELECT ?awardLabel ?year ?image WHERE { ?person wdt:P31 wd:Q5 ; rdfs:label \"%s\"@en ; wdt:P18 ?image . ?person p:P166 ?a . ?a ps:P166 ?award . ?a pq:P585 ?year . OPTIONAL { ?a pq:P805 ?ceremony . ?ceremony rdfs:label ?ceremony_label . FILTER (lang(?ceremony_label) = 'en') } ?award rdfs:label ?awardLabel . FILTER (lang(?awardLabel) = 'en' && CONTAINS(?awardLabel, \"Grammy\")) ?award schema:description ?awardDescription . FILTER (lang(?awardDescription) = 'en') }""" % suggestion

    



    try:
        results = get_results(endpoint_url, sparql_query)
        processed_data = process_data(results)
        print(sparql_query)
        print(processed_data)


    except Exception as e:
        print(e,"Attempt 1 has failed")    

        


    if not processed_data['awards']:
        try:
            qid = qid_dict[suggestion]

            sparql_query2 = """SELECT ?awardLabel ?year ?image WHERE { wd:%s wdt:P31 wd:Q5 ; wdt:P18 ?image . wd:%s p:P166 ?a . ?a ps:P166 ?award . ?a pq:P585 ?year . OPTIONAL { ?a pq:P805 ?ceremony . ?ceremony rdfs:label ?ceremony_label . FILTER (lang(?ceremony_label) = 'en') } ?award rdfs:label ?awardLabel . FILTER (lang(?awardLabel) = 'en' && CONTAINS(?awardLabel, "Grammy")) ?award schema:description ?awardDescription . FILTER (lang(?awardDescription) = 'en') }"""% (qid, qid)

             
            results = get_results(endpoint_url, sparql_query2)
            processed_data = process_data(results)

        except  Exception as e:
            print(e,"Attempt 2 has failed") 

        try: 
            qid = qid_dict[suggestion]

            sparql_query3 ="""SELECT ?awardLabel ?year ?image WHERE { BIND(wd:%s AS ?entity) ?entity wdt:P18 ?image . ?entity p:P166 ?a . ?a ps:P166 ?award . ?a pq:P585 ?year . OPTIONAL { ?a pq:P805 ?ceremony . ?ceremony rdfs:label ?ceremony_label . FILTER (lang(?ceremony_label) = 'en') } ?award rdfs:label ?awardLabel . FILTER (lang(?awardLabel) = 'en' && CONTAINS(?awardLabel, "Grammy")) ?award schema:description ?awardDescription . FILTER (lang(?awardDescription) = 'en') }"""% (qid)

            results = get_results(endpoint_url, sparql_query3)
            processed_data = process_data(results)

            if not processed_data['awards']:
                processed_data['awards'] = "no information found"  

        except  Exception as e:
            print(e,"Attempt 3 has failed") 
            processed_data['awards'] = "no information found"    
      
            


    
       
    return jsonify(processed_data)
    
     

 


   



    fuseki_result=fueski_query_execution((query))