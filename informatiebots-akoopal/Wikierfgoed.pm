package Wikierfgoed;

use strict;

require Exporter;

our @ISA=qw(Exporter);

our @EXPORT=qw(checkredirect checkdp checkfoto checkinfobox checkcommonscat checkcoordinaten checkiw checkdhm checkmdb checkmdbbe);

our $VERSION=0.01;

sub checkredirect {
  my $artikel = shift;

  if ( $artikel =~  m/doorverwijzing|redirect/i) {
    return 'Ja';
  } else {
    return 'Nee';
  }
}

sub checkdp {
  my $artikel = shift;

  if ( $artikel =~  m/\{\{dp\}\}/i) {
    return 'Ja';
  } else {
    return 'Nee';
  }
}

sub checkfoto {
  my $artikel = shift;

  if ( $artikel =~  m/([iI]mage|[aA]fbeelding|[fF]ile|[bB]estand):/) {
    return 'Ja';
  } elsif ( $artikel =~  m/afbeelding\s*=\s*\w/) {
    return 'Ja';
  } else {
    return 'Nee';
  }
}

sub checkinfobox {
  my $artikel = shift;
  my $object = shift;

  if ( $artikel =~  m/[iI]nfobox $object/) {
    return 'Ja';
  } else {
    return 'Nee';
  }
}

sub checkcommonscat {
  my $naam = shift;
  my $artikel = shift;
  my $commonseditor = shift;
  my $tmp;
  my $tmp2;

  if ( ($tmp) = ( $artikel =~  m/\{\{[cC]ommonscat[^|\}]*\|([^|\}]+)[|\}]/)) {
    ;
  } elsif ( $artikel =~  m/\{\{[cC]ommonscat\}\}/) {
    $tmp = $naam;
  } else {
    return 'Nee';
  }
  # Bestaat de commonscat
  $tmp2 = $commonseditor->get_text("Category:$tmp");

  if ( $tmp2 eq "2" ) {
    return "[[commons:Category:$tmp|{{Tekstkleur|#CC2200|$tmp}}]]";
  } else {
    return "[[commons:Category:$tmp|$tmp]]";
  }
}

sub checkcoordinaten {
  my $artikel = shift;
  my $coordinaten;
  my $coordinatenn;
  my $coordinatennm;
  my $coordinatenns;
  my $coordinatennl;
  my $coordinatene;
  my $coordinatenem;
  my $coordinatenes;
  my $coordinatenel;

  # Coordinaten in artikel?
  if ( ( $coordinatenn, $coordinatennm, $coordinatenns, $coordinatennl, $coordinatene, $coordinatenem, $coordinatenes, $coordinatenel ) = $artikel =~  m/\{\{[cC]o.rdinaten\|([\d\.]+)_([\d\.]+)_([\d\.]+)_([NS])_([\d\.]+)_([\d\.]+)_([\d\.]+)_([EW])_([Tt]ype|[Zz]oom|[Ss]cale|[[Rr]egion)/ ) {
    $coordinatenn += $coordinatennm/60 + $coordinatenns/3600;
    if ( $coordinatennl eq "S" ) { $coordinatenn *= -1 };
    $coordinatene += $coordinatenem/60 + $coordinatenes/3600;
    if ( $coordinatenel eq "W" ) { $coordinatene *= -1 };
    $coordinaten = "{{coor dec|$coordinatenn|$coordinatene|scale:12500}}";
  } elsif ( ( $coordinatenn, $coordinatennm, $coordinatennl, $coordinatene, $coordinatenem, $coordinatenel ) = $artikel =~  m/\{\{[cC]o.rdinaten\|([\d\.]+)_([\d\.]+)_([NS])_([\d\.]+)_([\d\.]+)_([EW])_([Tt]ype|[Zz]oom|[Ss]cale|[[Rr]egion)/ ) {
    $coordinatenn += $coordinatennm/60;
    if ( $coordinatennl eq "S" ) { $coordinatenn *= -1 };
    $coordinatene += $coordinatenem/60;
    if ( $coordinatenel eq "W" ) { $coordinatene *= -1 };
    $coordinaten = "{{coor dec|$coordinatenn|$coordinatene|scale:12500}}";
  } elsif ( ( $coordinatenn, $coordinatennl, $coordinatene, $coordinatenel ) = $artikel =~  m/\{\{[cC]o.rdinaten\|([\d\.]+)_([NS])_([\d\.]+)_([EW])_([Tt]ype|[Zz]oom|[Ss]cale|[[Rr]egion)/ ) {
    if ( $coordinatennl eq "S" ) { $coordinatenn *= -1 };
    if ( $coordinatenel eq "W" ) { $coordinatene *= -1 };
    $coordinaten = "{{coor dec|$coordinatenn|$coordinatene|scale:12500}}";
  } elsif ( ( $coordinatenn, $coordinatene ) = $artikel =~  m/\{\{[cC]oor[ _]title[ _]dec\|([\d\.]+)\|([\d\.]+)\|/ ) {
    $coordinaten = "{{coor dec|$coordinatenn|$coordinatene|scale:12500}}";
  } elsif ( ( $coordinatenn, $coordinatene ) = $artikel =~  m/\{\{[cC]o.rdinaten[ _]dec\|([\d\.]+)\|([\d\.]+)\|/ ) {
    $coordinaten = "{{coor dec|$coordinatenn|$coordinatene|scale:12500}}";
  } elsif ( ( $coordinatenn, $coordinatennm, $coordinatenns, $coordinatennl, $coordinatene, $coordinatenem, $coordinatenes, $coordinatenel ) = $artikel =~  m/\{\{[cC]o.r[ _]title[ _]dms\|([\d\.]+)\|([\d\.]+)\|([\d\.]+)\|([NS])\|([\d\.]+)\|([\d\.]+)\|([\d\.]+)\|([EW])\|/ ) {
    $coordinatenn += $coordinatennm/60 + $coordinatenns/3600;
    if ( $coordinatennl eq "S" ) { $coordinatenn *= -1 };
    $coordinatene += $coordinatenem/60 + $coordinatenes/3600;
    if ( $coordinatenel eq "W" ) { $coordinatene *= -1 };
    $coordinaten = "{{coor dec|$coordinatenn|$coordinatene|scale:12500}}";
  } elsif ( ( $coordinatenn, $coordinatennm, $coordinatennl, $coordinatene, $coordinatenem, $coordinatenel ) = $artikel =~  m/\{\{[cC]o.r[ _]title[ _]dm\|([\d\.]+)\|([\d\.]+)\|([NS])\|([\d\.]+)\|([\d\.]+)\|([EW])\|/ ) {
    $coordinatenn += $coordinatennm/60;
    if ( $coordinatennl eq "S" ) { $coordinatenn *= -1 };
    $coordinatene += $coordinatenem/60;
    if ( $coordinatenel eq "W" ) { $coordinatene *= -1 };
    $coordinaten = "{{coor dec|$coordinatenn|$coordinatene|scale:12500}}";
  } else {
    $coordinaten='Nee';
  }

  return $coordinaten;
}

sub checkiw {
  my $artikel = shift;
  my $language = shift;
  my $tmp;

  if ( ($tmp) = ( $artikel =~  m/\[\[$language:([^\[]*)\]\]/ )) {
    return "[[:en:$tmp]]";
  } else {
    return 'Nee';
  }
}

sub checkdhm {
  my $artikel = shift;
  my $tmp;

  if ( ($tmp) = ( $artikel =~  m|www.molens.nl/dbase/molen.php\?[^ ]*molenid=(\d+)|i )) {
    return "{{Link molendatabase-Hollandsche Molen\|id=$tmp|label=$tmp}}";
  } elsif ( ( $tmp ) = ( $artikel =~ m/\n\|[ \t]*molendatabase-Hollandsche Molen[ \t]*=[ \t]*(\S[^\n]*)\n[\|\}]/ ) ) {
    return "{{Link molendatabase-Hollandsche Molen\|id=$tmp|label=$tmp}}";
  } elsif ( ($tmp) = ( $artikel =~  m/{{Link molendatabase-Hollandsche Molen\|id=(\d+)/i )) {
    return "{{Link molendatabase-Hollandsche Molen\|id=$tmp|label=$tmp}}";
  } else {
    return 'Nee';
  }
}

sub checkmdb {
  my $artikel = shift;
  my $tmp;

  if ( ($tmp) = ( $artikel =~ m|www.molendatabase.nl/nederland/molen.php\?nummer=(\d+)|i)) {
    return "{{Link molendatabase-nl\|id=$tmp|label=$tmp}}";
  } elsif ( ( $tmp ) = ( $artikel =~ m/\n\|[ \t]*molendatabase-nl-windmotoren[ \t]*=[ \t]*(\S[^\n]*)\n[\|\}]/ ) ) {
    return "{{Link molendatabase-nl-windmotoren\|id=$tmp|label=wm$tmp}}";
  } elsif ( ( $tmp ) = ( $artikel =~ m/\n\|[ \t]*molendatabase-nl[ \t]*=[ \t]*(\S[^\n]*)\n[\|\}]/ ) ) {
    return "{{Link molendatabase-nl\|id=$tmp|label=$tmp}}";
  } elsif ( ($tmp) = ( $artikel =~  m/{{Link molendatabase-nl-windmotoren\|id=(\d+)/i )) {
    return "{{Link molendatabase-nl-windmotoren\|id=$tmp|label=wm$tmp}}";
  } elsif ( ($tmp) = ( $artikel =~  m/{{Link molendatabase-nl\|id=(\d+)/i )) {
    return "{{Link molendatabase-nl\|id=$tmp|label=$tmp}}";
  } else {
    return 'Nee';
  }
}

sub checkmdbbe {
  my $artikel = shift;
  my $tmp;

  if ( ($tmp) = ( $artikel =~ m|www.molenechos.org/molen.php\?AdvSearch=(\d+)|i)) {
    return "{{Link molendatabase-be\|id=$tmp|label=$tmp}}";
  } elsif ( ( $tmp ) = ( $artikel =~ m/\n\|[ \t]*molendatabase-be[ \t]*=[ \t]*(\S[^\n]*)\n[\|\}]/ ) ) {
    return "{{Link molendatabase-be\|id=$tmp|label=$tmp}}";
  } elsif ( ($tmp) = ( $artikel =~  m/{{Link molendatabase-be\|id=(\d+)/i )) {
    return "{{Link molendatabase-be\|id=$tmp|label=$tmp}}";
  } else {
    return 'Nee';
  }
}
