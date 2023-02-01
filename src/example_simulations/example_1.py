

categories='''
    category social();
    category economic();
    category political();
'''


distributions='''
    distribution di(expon, scale: 20);
    distribution block(uniform, scale: 50);
    distribution unemployment(expon, scale: 75);
    distribution we(expon,scale:30);
    distribution pg(expon,scale:30);
    distribution mortality([7]);
    distribution migration([7]);
    distribution PIB([365]);
    distribution taxes([30]);
    


'''


nations='''
    nation Cuba(11256372, 109884 , [], [], aviable_economic_resources:112000, industrialization: 30 , PIB:  45510000000, tourism:80, average_living_standard:50, life_expectancy: 76, employment: 97.2, poverty_level: 4.5, inflation: 3.67, crime_rate: 4.4, total_migration: 1);
    nation USA(331449281, 337341954, [], [], aviable_economic_resources:834500000, industrialization: 78 , PIB:15700000000000000, tourism:70, average_living_standard:94, life_expectancy: 73, employment: 94.5, poverty_level: 10.5, inflation: 1.5, crime_rate: 5, total_migration: 1);
    nation Canada(38246108, 9984670, [], [USA], aviable_economic_resources:53120000, industrialization: 72 , PIB:2027371000000, tourism:30, average_living_standard:94, life_expectancy: 82, employment: 98.5, poverty_level: 10, inflation: 2.1, crime_rate: 5.1, total_migration: 1);
    nation Mexico(128455567, 1964375 , [], [USA], aviable_economic_resources:93410000, industrialization: 63 , PIB:2890685000000, tourism:70, average_living_standard:68, life_expectancy: 70, employment: 94.9, poverty_level: 52.4 , inflation: 4.2, crime_rate: 8.7, total_migration: 1);

'''


decisions = ''' 

    decision event industrialization_increases(economic)<<n>>{
        inversion  =  n->extension * 0.0002;
        n->aviable_economic_resources = n-> aviable_economic_resources - inversion;
        n->industrialization = n->industrialization * 1.2;
        n->inflation=n->inflation*0.95;
    }    
    decision industrialization_increases_dec(n->aviable_economic_resources >= n->extension * 0.0002, industrialization_increases)<< n >>;

    decision event build_tourist_spots(economic)<<n>>{
        inversion = n->extension * 0.0002;
        n->aviable_economic_resources = n->aviable_economic_resources-inversion;
        n->tourism = n->tourism * 1.2;
    }
    decision build_tourist_spots_dec(n->aviable_economic_resources >= n->extension*0.0002, build_tourist_spots)<< n >>;

    decision event social_investments(social)<<n>>{
        inversion = n->population * 0.0002;
        n->aviable_economic_resources = n->aviable_economic_resources-inversion;
        n->poverty_level = n->poverty_level*0.9;
        n->life_expectancy = n->life_expectancy * 1.1;
        n->average_living_standard = n->average_living_standard*1.2;
    }    
    decision social_investments_dec(n->aviable_economic_resources >= n->population * 0.0002, social_investments)<< n >>;

    decision event create_jobs(social)<<n>>{
        inversion = 1/n -> employment * 1000;
        n->poverty_level=n->poverty_level * 0.9;
        n->aviable_economic_resources = n->aviable_economic_resources-inversion;
        n->employment = n->employment*1.2;
    }
    decision create_jobs_dec(n->aviable_economic_resources >= 10000, create_jobs)<< n >>;


'''


events='''

    simulation event unemployment_increases(unemployment, social, true, []){
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

    simulation event worsening_economy(we,economic,true,[]){        
        foreach <<nat>> (map->nations){
            
            nat->industrialization=nat->industrialization*0.9;
            nat->tourism=nat->tourism*0.9;
            nat->inflation=nat->inflation*1.1;
            nat->employment=nat->employment*0.9;
            nat->poverty_level=nat->poverty_level*1.1;
        }
    }

    simulation event decrease_industrialization(di, economic, true,[]){
        foreach <<nat>> (map->nations){
            nat->industrialization = nat->industrialization * 0.95;
        }
    }

    simulation event blockade_effects(block, economic, true,[]){        
        foreach <<nat>> (map->nations){
            if nat == Cuba {
                nat->industrialization = nat->industrialization * 0.9;
                nat->tourism = nat->tourism * 0.9;
                nat->average_living_standard = nat->average_living_standard * 0.9;
                nat->inflation= nat->inflation * 1.1;
            }
        }
    }

    simulation event population_mortality(mortality, social, true, []){
        foreach <<nat>> (map->nations){
            nat->population = nat->population - irvs(expon, loc: 0);
        }
    }

    simulation event population_migration(migration, social, true ,[]){
        foreach <<nat>> (map->nations){
            balance = (75 - nat->life_expectancy) + (100 - nat->employment) + (nat->poverty_level - 10)*5 + (nat->inflation-10) - (nat->crime_rate-5)*10 + (100-nat->average_living_standard)*5;
            rv = irvs(uniform, loc: balance * 10);
            nat->population = nat->population - rv;
            nat->total_migration = nat->total_migration + rv;
        }    
    }

     simulation event recalculate_PIB (PIB, social, true ,[]){
            foreach <<nat>> (map->nations){
            balance = (nat->employment-70)*500 + (10 - nat->poverty_level)*2000 + (10 - nat->inflation)*2000 + (nat->tourism-50)*1000 + (nat->industrialization-50)*1000;
            nat->PIB = nat->PIB + balance;
            nat->PIB = irvs(expon, loc: nat->PIB);
        }
    }

    simulation event collect_taxes(taxes, social, true ,[]){
        foreach <<nat>> (map->nations){
            increment = (nat->tourism-50)*1000 + (nat->industrialization-50)*1000;
            increment = irvs(uniform, loc: increment);
            nat->aviable_economic_resources = nat->aviable_economic_resources + increment;
        }
    }


'''


simulate= 'simulate(1y,5);'


plots='''
    plot(log1,  USA, ['average_living_standard','tourism']  , 'line');
    plot([log1,log2], [Cuba, Canada], 'average_living_standard' , 'bar');
    plot(logs->all, [Cuba,Canada], 'average_living_standard', 'dataframe');
    plot(Cuba, ['tourism', 'industrialization'] , 'line');

'''













