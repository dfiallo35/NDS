

decisions = '''

decision event industrialization_increases(economic)<<n>>{
        n->aviable_economic_resources = n->aviable_economic_resources-500;
        n->industrialization = n->industrialization*1.2;
    }    
    decision industrialization_increases_dec(n->aviable_economic_resources >= 5000, industrialization_increases)<< n >>;

    decision event tourism_increases(economic)<<n>>{
        n->aviable_economic_resources = n->aviable_economic_resources-7000;
        n->tourism = n->tourism*1.2;
    }
    decision tourism_increases_dec(n->aviable_economic_resources >= 7000, tourism_increases)<< n >>;

    decision event average_living_standard_increases(economic)<<n>>{
        n->aviable_economic_resources = n->aviable_economic_resources-6000;
        n->life_expectancy= n->life_expectancy*1.2;
        n->average_living_standard = n->average_living_standard*1.2;
    }    
    decision average_living_standard_increases_dec(n->aviable_economic_resources >= 6000, average_living_standard_increases)<< n >>;

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