
events='''

    simulation event unemployment_increases(pg, social, true, []){
        foreach <<nat>> (map->nations){
        nat->employment= nat->employment*0.9;
        nat->average_living_standard= nat->average_living_standard*0.9;
        }
    }

    simulation event population_growth(pg, social, true, []){
        foreach <<nat>> (map->nations){
            nat->population= irvs(expon, loc: nat->population);
        }
    }

    simulation event decrease_industrialization(pg,economic,true,[]){
        foreach <<nat>> (map->nations){
            nat->industrialization=nat->industrialization*0.9;
        }
    }

    simulation event intensification_of_the_blockade(block,economic,true,[]){        
        foreach <<nat>> (map->nations){
            if nat == Cuba {
                nat->industrialization=nat->industrialization*0.9;
                nat->tourism=nat->average_living_standard*0.9;
                nat->average_living_standard=nat->average_living_standard*0.9;
            }
        }
    }

    simulation event population_mortality(pg, social, true, []){
        foreach <<nat>> (map->nations){
            nat->population= nat->population - irvs(expon, loc: 0);
        }
    }
'''