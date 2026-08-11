import requests
import pandas as pd

API_KEY = ""
HEADERS = {'x-apisports-key': API_KEY}
BASE_URL = "https://v3.football.api-sports.io"

def fetch_premier_league_stats(league_id=39, season=2025):
    url = f"{BASE_URL}/players/topscorers"
    params = {'league': league_id, 'season': season}
    
    print(f"Fetching live Premier League data (League {league_id}, Season {season})...")
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Print any API notices
    errors = data.get('errors')
    if errors and (isinstance(errors, dict) and len(errors) > 0 or isinstance(errors, list) and len(errors) > 0):
        print(f"⚠️ API Error/Warning: {errors}")
        
    response_items = data.get('response', [])
    if not response_items:
        print("⚠️ No player data returned for this query yet.")
        return pd.DataFrame()

    player_list = []
    for item in response_items:
        player = item['player']
        stats = item['statistics'][0]  # Premier League stats block
        
        minutes = stats.get('games', {}).get('minutes') or 0
        goals = stats.get('goals', {}).get('total') or 0
        assists = stats.get('goals', {}).get('assists') or 0
        tackles = stats.get('tackles', {}).get('total') or 0
        
        # Expected Goals (xG)
        raw_xg = stats.get('goals', {}).get('expected')
        xg = float(raw_xg) if raw_xg is not None else 0.0
        
        player_list.append({
            'Player': player.get('name'),
            'Team': stats.get('team', {}).get('name'),
            'Position': stats.get('games', {}).get('position'),
            'Minutes': minutes,
            'Goals': goals,
            'Assists': assists,
            'xG': round(xg, 2),
            'Tackles': tackles,
            'Rating': float(stats.get('games', {}).get('rating') or 0),
        })
    
    df = pd.DataFrame(player_list)
    
    if df.empty:
        return df

    # --- Calculate Per 90 Metrics ---
    mask_90 = df['Minutes'] >= 90
    df['90s_Played'] = (df['Minutes'] / 90).round(2)
    
    # Goals per 90
    df['Goals_Per_90'] = 0.0
    df.loc[mask_90, 'Goals_Per_90'] = (df['Goals'] / df['90s_Played']).round(2)
    
    # xG per 90
    df['xG_Per_90'] = 0.0
    df.loc[mask_90, 'xG_Per_90'] = (df['xG'] / df['90s_Played']).round(2)
    
    # Tackles per 90
    df['Tackles_Per_90'] = 0.0
    df.loc[mask_90, 'Tackles_Per_90'] = (df['Tackles'] / df['90s_Played']).round(2)
    
    return df

if __name__ == "__main__":
    df = fetch_premier_league_stats(season=2025)
    
    if not df.empty:
        df.to_csv("pl_players_2025.csv", index=False)
        print("\n✅ Live 2025/2026 data successfully saved to 'pl_players_2025.csv'!")
        
        print("\n--- Top Performers Preview (2026/2027 Season) ---")
        top_goals = df.sort_values(by='Goals_Per_90', ascending=False)
        print(top_goals[['Player', 'Team', 'Position', 'Minutes', 'Goals', 'Goals_Per_90', 'xG_Per_90', 'Tackles_Per_90']].head(10))
    else:
        print("\n❌ Could not retrieve player statistics.")