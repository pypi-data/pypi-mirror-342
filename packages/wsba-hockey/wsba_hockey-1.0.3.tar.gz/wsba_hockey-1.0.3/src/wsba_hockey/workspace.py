import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import wsba_hockey as wsba
from gspread_pandas import Spread, Client
import urllib.request
from wand.color import Color
from wand.image import Image
from tools.xg_model import wsba_xG

season_load = wsba.repo_load_seasons()

def workspace(seasons,type,arg = '',start='',end=''):
    if type == 'pbp':
        #Scrape pbp
        errors=[]
        for season in seasons:
            data = wsba.nhl_scrape_season(season,remove=[],local=True,errors=True)
            errors.append(data['errors'])
            data['pbp'].to_csv(f'pbp/nhl_pbp_{season}.csv',index=False)
        print(f'Errors: {errors}')

    elif type == 'pbp_xg':
        #Add xG to pbp
        for season in seasons:
            print(f'WSBA xG for {season}')
            data = pd.read_parquet(f'pbp/parquet/nhl_pbp_{season}.parquet')
            wsba_xG(data).to_parquet(f'pbp/parquet/nhl_pbp_{season}.parquet',index=False)

    elif type == 'convert':
        for season in seasons:
            data = pd.read_csv(f"pbp/nhl_pbp_{season}.csv")
            data = wsba.wsba_main.moneypuck_xG(data)
            data.to_parquet(f'pbp/parquet/nhl_pbp_{season}.parquet',index=False)

    elif type == 'team_info':
        #Scrape team info
        stand = [wsba.nhl_scrape_standings(season) for season in seasons]
        standings = pd.concat(stand)
        
        colors = pd.read_csv('teaminfo/nhl_colors.csv')
        data = pd.merge(colors,standings,how='right',left_on='triCode',right_on='teamAbbrev.default').sort_values(by=['seasonId','triCode'])
        data['WSBA'] = data['teamAbbrev.default']+data['seasonId'].astype(str)

        data.to_csv('teaminfo/nhl_teaminfo.csv',index=False)
    
    elif type == 'stats':
        #Stats building
        for group in ['skater','team']:
            stats = []
            for season in seasons:
                pbp = pd.read_parquet(f'pbp/parquet/nhl_pbp_{season}.parquet')
                stat = wsba.nhl_calculate_stats(pbp,group,[2],['5v5'],shot_impact=True)
                stat.to_csv(f'stats/{group}/wsba_nhl_{season}_{group}.csv',index=False)
                stats.append(stat) 

            if arg:
                pd.concat(stats).to_csv(f'stats/db/wsba_nhl_{group}_db.csv',index=False)

    elif type == 'xg_model':
        data = pd.concat([pd.read_parquet(f'pbp/parquet/nhl_pbp_{season}.parquet') for season in seasons])
        wsba.wsba_main.wsba_xG(data,True,True)
        
    elif type == 'plot_game':
        for season in seasons:
            pbp = wsba.nhl_scrape_season(season,remove=[],start=start,end=end)

            plots = wsba.nhl_plot_games(pbp,wsba.wsba_main.fenwick_events,['5v5'],'all',team_colors=arg,legend=False,xg='wsba')

            games = list(pbp['game_id'].astype(str).drop_duplicates())
            i = 1
            for plot, game_id in zip(plots,games):
                plot.savefig(f'plots/games/{game_id[0:4]}{int(game_id[0:4])+1}/{game_id[5:6]}/{game_id}_shotplot.png',bbox_inches='tight',transparent=True)
                i += 1
    
    elif type == 'plot_skater':
        for season in seasons:
            pbp = pd.read_parquet(f'pbp/parquet/nhl_pbp_{season}.parquet')

            skaters={}

            for shooter,season,team in zip(pbp['event_player_1_name'],pbp['season'].astype(str),pbp['event_team_abbr']):    
                if shooter is None:
                    continue
                else:
                    skaters.update({
                        shooter:[season,team]
                    })

            plots = wsba.nhl_plot_skaters_shots(pbp,skaters,['5v5'],onice='indv',title=False,legend=True)

            items = list(skaters.items())
            for plot,skater in zip(plots,items):
                plot.savefig(f'plots/{skater[1][0]}/{skater[0]}{skater[1][0]}{skater[1][1]}_indv.png',bbox_inches='tight',transparent=True)
    
    elif type == 'logos':
        data = pd.read_csv('teaminfo/nhl_teaminfo.csv')
        for url, id in zip(data['teamLogo'],data['WSBA']):
            print(url)
            urllib.request.urlretrieve(url,f'tools/logos/svg/{id}.svg')
            with Image(filename=f'tools/logos/svg/{id}.svg') as img:
                img.format = 'png32'
                img.background_color = Color('transparent')  
                img.alpha_channel = 'activate'    
                img.save(filename=f'tools/logos/png/{id}.png')
                
    else:
        print('Nothing here.')

def push_to_sheet():
    spread = Spread('WSBA - NHL 5v5 Shooting Metrics Public v2.0')

    #Tables
    skater = pd.read_csv('stats/db/wsba_nhl_skater_db.csv')
    team = pd.read_csv('stats/db/wsba_nhl_team_db.csv')
    team_info = pd.read_csv('teaminfo/nhl_teaminfo.csv')
    country = pd.read_csv('teaminfo/nhl_countryinfo.csv')
    schedule = pd.read_csv('schedule/schedule.csv')

    spread.df_to_sheet(skater,index=False,sheet='Skaters DB')
    spread.df_to_sheet(team,index=False,sheet='Teams DB')
    spread.df_to_sheet(team_info,index=False,sheet='Team Info')
    spread.df_to_sheet(country,index=False,sheet='Country Info')
    spread.df_to_sheet(schedule,index=False,sheet='Schedule')

    print('Done.')

workspace(season_load[6:18],,Tru)