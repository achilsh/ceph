#!/usr/bin/perl

use CrushWrapper;
use Config::General;
use Tie::IxHash;
use Data::Dumper;

tie my %conf, "Tie::IxHash";

my $wrap = new CrushWrapper::CrushWrapper;

my $alg_types = {
	uniform => 1,
	list => 2, 
	tree => 3, 
	straw => 4
};

$wrap->create();

%conf = Config::General::ParseConfig( -ConfigFile => "sample.txt", -Tie => "Tie::IxHash", -MergeDuplicateBlocks => 1 );

my $arr = \%conf;
print Dumper $arr;

my @ritems;


# find lowest id number used
sub get_lowest {
	my $item = shift;
	return unless ref $item;

	my $lowest = 0;

	if (ref $item eq 'HASH') { 
		$lowest = $item->{'id'} if $lowest > $item->{'id'};
		foreach my $key (keys %{$item}) { 
			#next if grep { $key eq $_ } qw(type rule);

			my $sublowest = get_lowest($item->{$key});
			$lowest = $sublowest if $lowest > $sublowest;
		}
	} elsif (ref $item eq 'ARRAY') { 
		foreach my $element (@{$item}) { 
			my $sublowest = get_lowest($element);
			$lowest = $sublowest if $lowest > $sublowest;
		}
	} 

	return $lowest;
}

my $lowest = get_lowest($arr);
#print "lowest is $lowest\n";


# add type names/ids 
foreach my $type (keys %{$arr->{'type'}}) {
	#print $wrap->get_type_name($arr->{'type'}->{$type}->{'id'}) ."\n";
}


# build item name -> id 
foreach my $section (qw(devices buckets)) { 
	foreach my $item_type (keys %{$arr->{$section}}) {
		foreach my $name (keys %{$arr->{$section}->{$item_type}}) {
			my $id = $arr->{$section}->{$item_type}->{$name}->{'id'};
			if ($section eq 'devices') { 
				if (!defined $id || $id < 0) { 
					die "invalid device id for $item_type $name: id is required and must be non-negative";
				}
			} else {
				if ($id > -1) { 
					die "invalid bucket id for $item_type $name: id must be negative";
				} elsif (!defined $id) { 
					# get the next lower ID number and inject it into the config hash
					$id = --$lowest;
					$arr->{$section}->{$item_type}->{$name}->{'id'} = $id;
				}
			}
			$wrap->set_item_name($id, $name);
		}
	}
}

foreach my $item_type (keys %{$arr->{'types'}->{'type'}}) {
	my $type_id = $arr->{'types'}->{'type'}->{$type}->{'type_id'};
	$wrap->set_type_name($type_id, $type);
}

foreach my $bucket_type (keys %{$arr->{'buckets'}}) {

	print "doing bucket type $type\n";
	foreach my $bucket_name (keys %{$arr->{'buckets'}->{$bucket_type}}) {
		print "... bucket: $bucket_name\n";

		my @item_ids;
		foreach my $item_name (keys %{$arr->{'buckets'}->{$bucket_type}->{$bucket_name}->{'item'}}) {
			push @item_ids, $wrap->get_item_id($item_name);
		}

		my $bucket_id = $arr->{'buckets'}->{$bucket_type}->{$bucket_name}->{'id'};
		my $alg = $arr->{'buckets'}->{$bucket_type}->{$bucket_name}->{'alg'};
		$alg = $alg_types->{'straw'} if !$alg;

		print "alg is: $alg\n";

		# bucket_id, alg, type, size, items, weights
		#TODO: pass the correct value for type to add_bucket
		my $result = $wrap->add_bucket($bucket_id, $alg, 0, scalar(@item_ids), \@item_ids, []);
		print "... $result\n\n";
	}   
}




=item

/*** BUCKETS ***/
enum {
    CRUSH_BUCKET_UNIFORM = 1,
    CRUSH_BUCKET_LIST = 2,
    CRUSH_BUCKET_TREE = 3,
    CRUSH_BUCKET_STRAW = 4
};

/*** RULES ***/
enum {
    CRUSH_RULE_NOOP = 0,
    CRUSH_RULE_TAKE = 1,          /* arg1 = value to start with */
    CRUSH_RULE_CHOOSE_FIRSTN = 2, /* arg1 = num items to pick */
                                  /* arg2 = type */
    CRUSH_RULE_CHOOSE_INDEP = 3,  /* same */
    CRUSH_RULE_EMIT = 4           /* no args */
};

=cut
