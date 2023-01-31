

categories='''
    category social();
    category economic();
    category political();
    category military();
    category territorial();
'''


distributions='''
    distribution pg(expon, scale: 20);
    distribution block(expon, scale: 50);

'''


nations='''
    nation Cuba(11256372, 109884 , [], [], aviable_economic_resources:112000, industrialization: 30 , PIB:  45510000000, tourism:80, average_living_standard:50, life_expectancy: 76, employment: 97.2, poverty_level: 4.5, inflation: 3.67, crime_rate: 4.4);
    nation USA(9147593, 337341954, [], [], aviable_economic_resources:834500000, industrialization: 78 , PIB:15700000000000000, tourism:70, average_living_standard:94, life_expectancy: 73, employment: 94.5, poverty_level: 10.5, inflation: 1.5, crime_rate: 5);
    nation Canada(38246108, 9984670, [], [USA], aviable_economic_resources:53120000, industrialization: 72 , PIB:2027371000000, tourism:30, average_living_standard:94, life_expectancy: 82, employment: 98.5, poverty_level: 10, inflation: 2.1, crime_rate: 5.1);
    nation Mexico(128455567, 1964375 , [], [USA], aviable_economic_resources:93410000, industrialization: 63 , PIB:2890685000000, tourism:70, average_living_standard:68, life_expectancy: 70, employment: 94.9, poverty_level: 52.4 , inflation: 4.2, crime_rate: 8.7);

'''


decisions = ''' 

    decision event industrialization_increases(economic)<<n>>{
        inversion=n->extension * 0.0002;
        n->aviable_economic_resources = n->aviable_economic_resources-inversion;
        n->industrialization = n->industrialization*1.2;
    }    
    decision industrialization_increases_dec(n->aviable_economic_resources >= n->extension * 0.0002, industrialization_increases)<< n >>;

    decision event build_tourist_spots(economic)<<n>>{
        inversion=n->extension * 0.0002;
        n->aviable_economic_resources = n->aviable_economic_resources-inversion;
        n->tourism = n->tourism * 1.2;
    }
    decision build_tourist_spots_dec(n->aviable_economic_resources >= extension*0.0002, build_tourist_spots)<< n >>;

    decision event social_investments(social)<<n>>{
        inversion = n->population * 0.0002;
        n->aviable_economic_resources = n->aviable_economic_resources-inversion;
        n->poverty_level = n->poverty_level*0.9;
        n->life_expectancy = n->life_expectancy * 1.1;
        n->average_living_standard = n->average_living_standard*1.2;
    }    
    decision social_investments_dec(n->aviable_economic_resources >= n->population * 0.0002, social_investments)<< n >>;

    decision event create_jobs(social)<<n>>{
        inversion = 1/n->employment * 1000;
        n->poverty_level=n->poverty_level * 0.9;
        n->aviable_economic_resources = n->aviable_economic_resources-inversion;
        n->employment = n->employment*1.2;
    }
    decision create_jobs_dec(n->aviable_economic_resources >= 10000, create_jobs)<< n >>;


'''


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

    simulation event worsening_economy(pg,economic,true,[]){        
        foreach <<nat>> (map->nations){
            
            nat->industrialization=nat->industrialization*0.9;
            nat->tourism=nat->tourism*0.9;
            nat->inflation=nat->inflation*1.1;
            nat->employment=nat->employment*0.9;
            nat->poverty_level=nat->poverty_level*1.1;
        }
    }

    simulation event decrease_industrialization(pg,economic,true,[]){
        foreach <<nat>> (map->nations){
            nat->industrialization=nat->industrialization*0.9;
        }
    }

    simulation event blockade_effects(block,economic,true,[]){        
        foreach <<nat>> (map->nations){
            if nat == Cuba {
                nat->industrialization=nat->industrialization*0.9;
                nat->tourism=nat->tourism*0.9;
                nat->average_living_standard=nat->average_living_standard*0.9;
                nat->inflation=nat->inflation*1.1;
            }
        }
    }

    simulation event population_mortality(pg, social, true, []){
        foreach <<nat>> (map->nations){
            nat->population= nat->population - irvs(expon, loc: 0);
        }
    }


    #IMPLEMENT
    # simulation event migration(pg,social, true ,[]){
    #     foreach <<nat>> (map->nations){
    #         nat->population
    #         employment
    #         average_living_standard

    #     }    
    # }

    # simulation event recalculate_PIB (pg,social, true ,[]){
    #     foreach <<nat>> (map->nations){
    #         nat->population
    #         employment
    #         average_living_standard

    #     }


    simulation event collect_taxes(pg,social, true ,[]){
        foreach <<nat>> (map->nations){
            increment=nat->industrialization * nat->tourism * nat->employment * nat->population / nat->extension;
            nat->aviable_economic_resources = nat->aviable_economic_resources+ increment;
        }
    }


'''


simulate= 'simulate(50d,5);'


plots='''
    plot(log1,  USA, ['average_living_standard','tourism']  , 'line');
    plot([log1,log2], [Cuba, Canada], 'average_living_standard' , 'bar');
    plot(logs->all, [Cuba,Canada], 'average_living_standard', 'dataframe');
    plot(Cuba, ['tourism', 'industrialization'] , 'line');

'''













