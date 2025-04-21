import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import wsba_hockey as wsba

season_load = wsba.repo_load_seasons()

def workspace(seasons,type):
    if type == 'pbp':
        #Scrape pbp
        errors=[]
        for season in seasons:
            data = wsba.nhl_scrape_season(season,remove=[],local=True,errors=True)
            errors.append(data['errors'])
            data['pbp'].to_csv(f'pbp/nhl_pbp_{season}.csv',index=False)
        print(f'Errors: {errors}')

    elif type == 'convert':
        for season in seasons[6:12]:
            data = pd.read_csv(f"pbp/nhl_pbp_{season}.csv")
            data = wsba.wsba_main.moneypuck_xG(data)
            data.to_parquet(f'pbp/parquet/nhl_pbp_{season}.parquet',index=False)

    elif type == 'standings':
        #Scrape standings
        stand = [wsba.nhl_scrape_standings(season) for season in season]
        pd.concat(stand).to_csv('teaminfo/nhl_standings.csv',index=False)
    
    elif type == 'stats':
        #Stats building
        stats = []
        for season in seasons[6:18]:
            for group in ['skater','team']:
                pbp = pd.read_parquet(f'pbp/parquet/nhl_pbp_{season}.parquet')
                stat = wsba.nhl_calculate_stats(pbp,group,[2],['5v5'],shot_impact=True)
                stat.to_csv(f'stats/{group}/wsba_nhl_{season}_{group}.csv',index=False)
                stats.append(stat)
            pd.concat(stats).to_csv(f'stats/db/wsba_nhl_{group}_db.csv',index=False)
    else:
        print('Nothing here.')

pbp = pd.read_parquet('pbp/parquet/nhl_pbp_20242025.parquet')

skaters={}

for shooter,season,team in zip(pbp['event_player_1_name'],pbp['season'].astype(str),pbp['event_team_abbr']):    
    if shooter is None:
        continue
    else:
        skaters.update({
            shooter:[season,team]
        })

plots = wsba.nhl_plot_skaters_shots(pbp,skaters,['5v5'],onice='indv',legend=True)

items = list(skaters.items())
for plot,skater in zip(plots,items):
    plt.title('')
    plot.savefig(f'plots/{skater[0]}{skater[1][0]}{skater[1][1]}_indv.png',bbox_inches='tight',transparent=True)

plots = wsba.nhl_plot_games(wsba.nhl_scrape_season('20242025',start='04-19',end='04-19'),wsba.wsba_main.fenwick_events,['5v5'],'all',legend=True)

i = 1
for plot in plots:
    plot.savefig(f'plots/20242025_03_{i}_shotplot.png',bbox_inches='tight',transparent=True)
    i += 1