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
my @loccats;
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
my $coordinaten;
my $coordinatenn;
my $coordinatene;
my $redirect;
my $dppagina;
my $commonscat;
my $tmp;

my @provincies = ("Groningen", "Friesland", "Drenthe", "Overijssel", "Gelderland", "Utrecht", "Noord-Holland", "Zuid-Holland", "Zeeland", "Noord-Brabant", "Limburg (Nederland)" );

  $paginastatuit = <<'EOF';
{| class="sortable wikitable vatop" style="font-size:90%;"
!Land
!Aantal kastelen
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
  $provincielijst = "Lijst van kastelen in $provincie";
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
!Infobox kasteel
!Coordinaten
!Commonscat
!Loc Cat
!Misc Cat
EOF

  @records = split (/\|\-.*\n\|/m, $pagina);

  foreach my $record (@records) {
    @fields = split (/\|\|/m, $record);
    if (@fields > 6) {
      $objectcount++;
      $fotoartikel = 'nvt';
      $objectsjabloon = 'nvt';
      $coordinaten = 'nvt';
      $redirect = 'nvt';
      $dppagina = 'nvt';
      $commonscat = 'nvt';
      @cats = ();
      @loccats = ();
      @misccats = ();

      # parse eerste veld voor artikelnaam en linknaam
      if ( $fields[0] =~ m/\[\[.*\|/ ) {
	($artikel,$naam) = ($fields[0] =~ m/\[\[([^\|]+)\|([^\]]+)\]\]/);
      } elsif ( $fields[0] =~ m/\[\[([^\|]+)\]\]/ ) {
	($naam) = ($fields[0] =~ m/\[\[([^\|]+)\]\]/);
	$artikel = $naam;
      } else {
	$artikel = "not linked";
	$naam = $fields[0];
      }
  
      # Tel afbeeldingen
      $fotolijst = checkfoto($fields[7]);
      $fotocount++ if ( $fotolijst eq 'Ja' );

      # Tel bestaande artikelen
      # print "$artikel|$naam\n";
      if ( $artikel ne "not linked" ) {
        $object = $editor->get_text($artikel);
        die("error bij $artikel:$editor->{errstr}\n") if ($editor->{errstr});
      } else {
	$object = "2";
      }
      if ( $object ne "2" ) {
	$artikelencount++;

	# foto in artikel?
	$fotoartikel = checkfoto($object);
	$fotoartcount++ if ( $fotoartikel eq 'Ja');

	# Infobox in artikel?
	$objectsjabloon = checkinfobox($object, 'kasteel');

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
	  if ( $cat =~ m/kasteel in/i ) { push @loccats, $cat; }
	  elsif ( $cat =~ m/borg in/i ) { push @loccats, $cat; }
	  elsif ( $cat =~ m/havezate in/i ) { push @loccats, $cat; }
	  elsif ( $cat =~ m/ridderhofstad/i ) { push @loccats, $cat; }
#	  elsif ( $cat =~ m/vaardig/i ) { push @statcats, $cat; }
	  else { push @misccats, $cat; };
	}
      }

      $paginauit = $paginauit."|-\n|$fields[0] || $fields[1] || $redirect || $dppagina || $fotolijst || $fotoartikel || $objectsjabloon || $coordinaten || $commonscat || ". join(", ", sort @loccats). " || ". join(", ", sort @misccats). "\n";

      # ff rust
      # sleep 4;

    }
  }

  $paginauit = "[[Gebruiker:Akoopal/Kastelenoverzicht|Overzicht]]<br>\n'''$provincie'''\n*Lijst: [[$provincielijst]]\n* Aantal kastelen in lijst: $objectcount\n* Aantal artikelen: $artikelencount\n* Aantal foto's in de lijst: $fotocount\n* Aantal foto's in een artikel: $fotoartcount\n".$paginauit."|}\n";
  # print $paginauit;
  $editor->edit("Gebruiker:Akoopal/Kastelen in $provincie",$paginauit,"Autorefreshed");

  $objectcounttotaal += $objectcount;
  $artikelencounttotaal += $artikelencount;
  $fotocounttotaal += $fotocount;
  $fotoartcounttotaal += $fotoartcount;
  $coordinatencounttotaal += $coordinatencount;

  print "$provincie heeft $objectcount kastelen, $artikelencount artikelen, $fotoartcount foto's in de artikelen en $fotocount foto's in de lijst\n";

  $paginastatuit = $paginastatuit."|-\n|[[Gebruiker:Akoopal/Kastelen in $provincie|$provincie]] || $objectcount || $artikelencount ||".int($artikelencount*100/$objectcount+.5)."%|| $fotocount ||".int($fotocount*100/$objectcount+.5)."%|| $fotoartcount||".int($fotoartcount*100/$objectcount+.5)."%|| $coordinatencount ||".int($coordinatencount*100/$objectcount+.5)."%\n";
}

$paginastatuit = "* Artikelen te gaan: ".($objectcounttotaal - $artikelencounttotaal)."\n* Foto's te gaan: ".($objectcounttotaal - $fotocounttotaal)."\n".$paginastatuit."|-\n|Totaal || $objectcounttotaal || $artikelencounttotaal ||".int($artikelencounttotaal*100/$objectcounttotaal+.5)."%|| $fotocounttotaal ||".int($fotocounttotaal*100/$objectcounttotaal+.5)."%|| $fotoartcounttotaal||".int($fotoartcounttotaal*100/$objectcounttotaal+.5)."%|| $coordinatencounttotaal ||".int($coordinatencounttotaal*100/$objectcounttotaal+.5)."%\n|}\n";

# print $paginastatuit;
$editor->edit("Gebruiker:Akoopal/Kastelenoverzicht",$paginastatuit,"Autorefreshed");
