#!/usr/bin/perl -w

use strict;
use Data::Dumper;
use MediaWiki::Bot;
use Wikierfgoed;
use Wikiauth;

my $editor = MediaWiki::Bot->new($wikiuser);
# $editor->{debug}=1;
$editor->set_wiki('nl.wikipedia.org','w');
$editor->login($wikiuser,$wikipass);

my $editor_c = MediaWiki::Bot->new($wikiuser);
$editor_c->set_wiki('commons.wikimedia.org','w');
$editor_c->login($wikiuser,$wikipass);

my $pagina;
my $paginauit;
my $paginastatuit;
my @records;
my @fields;
my $artikel;
my $naam;
my $object;
my $provincielijst;
my @cats;
my $cat;
my @statcats;
my @loccats;
my @funccats;
my @typecats;
my @misccats;

my $objectcount;
my $artikelencount;
my $fotocount;
my $fotoartcount;
my $coordinatencount;

my $objectcounttotaal = 0;
my $artikelencounttotaal = 0;
my $fotocounttotaal = 0;
my $fotoartcounttotaal = 0;
my $coordinatencounttotaal = 0;

my $fotolijst;
my $fotoartikel;
my $objectsjabloon;
my $molendb;
my $dhmlink;
my $coordinaten;
my $coordinatenn;
my $coordinatene;
my $redirect;
my $dppagina;
my $commonscat;
my $tmp;

my @provincies = ("Overijssel", "Gelderland", "Zeeland", "Noord-Brabant", "Limburg (Nederland)" );
#my @provincies = ("Groningen", "Friesland", "Drenthe", "Overijssel", "Gelderland", "Utrecht", "Noord-Holland", "Zuid-Holland", "Zeeland", "Noord-Brabant", "Limburg" );

  $paginastatuit = <<'EOF';
{| class="sortable wikitable vatop" style="font-size:90%;"
!Provincie
!Aantal molens
!Artikelen
!%
!Foto's in lijst
!%
!Foto's in artikel
!%
!Artikelen met coordinaten
!%
EOF

foreach my $provincie (@provincies) {
  $provincielijst = "Sjabloon:Tabeldata lijst van voormalige watermolens in $provincie";
  $pagina = $editor->get_text($provincielijst);

  if ( $pagina eq "2" ) {
    print "error fetching $provincie\n";
    next;
  }
  
  $fotocount = 0;
  $fotoartcount = 0;
  $objectcount = 0;
  $artikelencount = 0;
  $coordinatencount = 0;

  $paginauit = <<'EOF';
{| class="sortable wikitable vatop" style="width:98%; font-size:90%;"
!Naam
!Plaats
!Redirect
!DP
!Foto in lijst
!Foto in artikel
!Infobox molen
!Link MDB
!Link DHM
!Coordinaten
!Commonscat
!Status Cat
!Loc Cat
!Type Cat
!Func Cat
!Misc Cat
EOF


  @records = split (/\|\-.*\n\|/m, $pagina);

  foreach my $record (@records) {
    @fields = split (/\|\|/, $record);
    if (@fields > 6) {
      $objectcount++;
      $fotoartikel = 'nvt';
      $objectsjabloon = 'nvt';
      $molendb = 'nvt';
      $dhmlink = 'nvt';
      $coordinaten = 'nvt';
      $redirect = 'nvt';
      $dppagina = 'nvt';
      $commonscat = 'nvt';
      @cats = ();
      @statcats = ();
      @loccats = ();
      @funccats = ();
      @typecats = ();
      @misccats = ();

      # parse eerste veld voor artikelnaam en linknaam
      if ( $fields[0] =~ m/\|/ ) {
	($artikel,$naam) = ($fields[0] =~ m/\[\[([^\|]+)\|([^\]]+)\]\]/);
      } else {
	($naam) = ($fields[0] =~ m/\[\[([^\|]+)\]\]/);
	$artikel = $naam;
      }
  
      # Tel afbeeldingen
      $fotolijst = checkfoto($fields[9]);
      $fotocount++ if ( $fotolijst eq 'Ja' );

      # Tel bestaande artikelen
      # print "$naam\n";
      $object = $editor->get_text($artikel);
      die("error bij $artikel:$editor->{errstr}\n") if ($editor->{errstr});
      if ( $object ne "2" ) {
	$artikelencount++;

	# foto in artikel?
	$fotoartikel = checkfoto($object);
	$fotoartcount++ if ( $fotoartikel eq 'Ja');

	# Infobox in artikel?
	$objectsjabloon = checkinfobox($object, 'molen');

	# molendatabase link in artikel?
	$molendb = checkmdb($object);

	# DHM link in artikel?
	$dhmlink = checkdhm($object);                                                   
	# Coordinaten in artikel?
	$coordinaten = checkcoordinaten($object);
	$coordinatencount++ if ( $coordinaten ne 'Nee');

	# Redirect in artikel?
	$redirect = checkredirect($object);

	# Artikel is doorverwijspagina?
	$dppagina = checkdp($object);

	# Artikel heeft commons categorie?
	$commonscat = checkcommonscat($artikel,$object,$editor_c);

	# Parse cats
	@cats = ( $object =~ m/\[\[[cC]ategor[^:]+:([^\]|]+)[\]|]/g );
	foreach $cat (@cats) {
	  $cat =~ s/_/ /g;
	  if ( $cat =~ m/molen in/i ) { push @loccats, $cat; }
	  elsif ( $cat =~ m/vaardig/i ) { push @statcats, $cat; }
	  elsif ( $cat =~ m/bovenslag|middenslag|onderslag|middenslag|turbine|getijdemolen/i ) { push @typecats, $cat; }
	  elsif ( $cat =~ m/oliemolen|korenmolen|papiermolen/i ) { push @funccats, $cat; }
	  else { push @misccats, $cat; };
	}
      }

      $paginauit = $paginauit."|-\n|$fields[0] || $fields[2] || $redirect || $dppagina || $fotolijst || $fotoartikel || $objectsjabloon || $molendb || $dhmlink || $coordinaten || $commonscat || ". join(", ", sort @statcats). " || ". join(", ", sort @loccats). " || ". join(", ", sort @typecats). " || ". join(", ", sort @funccats). " || ". join(", ", sort @misccats). "\n";

      # ff rust
      # sleep 4;

    }
  }

  $paginauit = "[[Gebruiker:Akoopal/Voormalige watermolenoverzicht|Overzicht]]<br>\n'''$provincie'''\n*Lijst: [[$provincielijst]]\n* Aantal molens in lijst: $objectcount\n* Aantal artikelen: $artikelencount\n* Aantal foto's in de lijst: $fotocount\n* Aantal foto's in een artikel: $fotoartcount\n* MDB = molendatabase, DHM=De Hollandse Molen\n".$paginauit."|}\n";
  # print $paginauit;
   $editor->edit("Gebruiker:Akoopal/Voormalige watermolens in $provincie",$paginauit,"Autorefreshed");

  $objectcounttotaal += $objectcount;
  $artikelencounttotaal += $artikelencount;
  $fotocounttotaal += $fotocount;
  $fotoartcounttotaal += $fotoartcount;
  $coordinatencounttotaal += $coordinatencount;

  print "$provincie heeft $objectcount molens, $artikelencount artikelen, $fotoartcount foto's in de artikelen en $fotocount foto's in de lijst\n";

  $paginastatuit = $paginastatuit."|-\n|[[Gebruiker:Akoopal/Voormalige watermolens in $provincie|$provincie]] || $objectcount || $artikelencount ||".int($artikelencount*100/$objectcount+.5)."%|| $fotocount ||".int($fotocount*100/$objectcount+.5)."%|| $fotoartcount||".int($fotoartcount*100/$objectcount+.5)."%|| $coordinatencount ||".int($coordinatencount*100/$objectcount+.5)."%\n";
}

$paginastatuit = "* Artikelen te gaan: ".($objectcounttotaal - $artikelencounttotaal)."\n* Foto's te gaan: ".($objectcounttotaal - $fotocounttotaal)."\n".$paginastatuit."|-\n|Totaal || $objectcounttotaal || $artikelencounttotaal ||".int($artikelencounttotaal*100/$objectcounttotaal+.5)."%|| $fotocounttotaal ||".int($fotocounttotaal*100/$objectcounttotaal+.5)."%|| $fotoartcounttotaal||".int($fotoartcounttotaal*100/$objectcounttotaal+.5)."%|| $coordinatencounttotaal ||".int($coordinatencounttotaal*100/$objectcounttotaal+.5)."%\n|}\n";

#print $paginastatuit;
$editor->edit("Gebruiker:Akoopal/Voormalige watermolenoverzicht",$paginastatuit,"Autorefreshed");
