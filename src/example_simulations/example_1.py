

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
    #nation Cuba(11256372, 109884 , [], [], aviable_economic_resources:112000, industrialization: 30 , PIB:  45510000000, tourism:80, average_living_standard:50, life_expectancy: 76, employment: 97.2, poverty_level: 4.5, inflation: 3.67, crime_rate: 4.4);
    nation USA(9147593, 337341954, [], [], aviable_economic_resources:834500000, industrialization: 78 , PIB:15700000000000000, tourism:70, average_living_standard:94,life_expectancy: 73, employment: 94.5, poverty_level: 10,5, inflation: 1.5, crime_rate: 5);
    nation Canada(38246108, 9984670, [], [USA], aviable_economic_resources:53120000, industrialization: 72 , PIB:2027371000000, tourism:30, average_living_standard:94,life_expectancy: 82, employment: 98.5, poverty_level: 10, inflation: 2.1, crime_rate: 5.1);
    nation Mexico(128455567, 1964375 , [], [USA], aviable_economic_resources:93410000, industrialization: 63 , PIB:2890685000000, tourism:70, average_living_standard:68,life_expectancy: 70, employment: 94.9, poverty_level: 52.4 , inflation: 4.2 , crime_rate: 8.7);

'''


decisions = ''' 

    decision event industrialization_increases(economic)<<n>>{
        inversion=n->extension/5000
        n->aviable_economic_resources = n->aviable_economic_resources-inversion;
        n->industrialization = n->industrialization*1.2;
    }    
    decision industrialization_increases_dec(n->aviable_economic_resources >= n->extension/5000, industrialization_increases)<< n >>;

    decision event tourism_increases(economic)<<n>>{
        inversion=n->extension/5000
        n->aviable_economic_resources = n->aviable_economic_resources-inversion;
        n->tourism = n->tourism*1.2;
    }
    decision tourism_increases_dec(n->aviable_economic_resources >= extension/5000, tourism_increases)<< n >>;

    decision event average_living_standard_increases(social)<<n>>{
        inversion=n->population/5000
        n->aviable_economic_resources = n->aviable_economic_resources-6000;
        n->life_expectancy= n->life_expectancy*1.2;
        n->average_living_standard = n->average_living_standard*1.2;
    }    
    decision average_living_standard_increases_dec(n->aviable_economic_resources >= n->population/5000, average_living_standard_increases)<< n >>;

    decision event create_jobs(social)<<n>>{
        n->aviable_economic_resources = n->aviable_economic_resources-4000;
        n->employment = n->employment*1.2;
    }
    decision create_jobs_dec(n->aviable_economic_resources >= 4000, create_jobs)<< n >>;

    decision event increment_aviable_economic_resources(social)<<n>>{
        a = n->PIB * 0.1;
        n->PIB = n->PIB - a;
        n->aviable_economic_resources = n->aviable_economic_resources + a;
    }    
    decision increment_aviable_economic_resources_dec(n->PIB >= n->population*100, increment_aviable_economic_resources)<< n >>;


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

    simulation event name migration(pg,social, true ,[]){
        foreach <<nat>> (map->nations){
            nat->population
            employment
            average_living_standard

        }    
    }

    simulation event name recalculatePIB (pg,social, true ,[]){
        foreach <<nat>> (map->nations){
            nat->population
            employment
            average_living_standard

        }

    simulation event name recalculatePIB (pg,social, true ,[]){
        foreach <<nat>> (map->nations){
            nat->population
            employment
            average_living_standard

        }

    simulation event name collect_taxes (pg,social, true ,[]){
        foreach <<nat>> (map->nations){
            nat->population
            employment
            average_living_standard

        }


'''


simulate= 'simulate(50d,5);'


plots='''
    plot(log1,  USA, ['average_living_standard','tourism']  , 'line');
    plot([log1,log2], [Cuba, Canada], 'average_living_standard' , 'bar');
    plot(logs->all, [Cuba,Canada], 'average_living_standard', 'dataframe');
    plot(Cuba, ['tourism', 'industrialization'] , 'line');

'''













