# Data collected from hearthscry
import os
import sys
import json
import csv
import pprint

hp_list = [
    'Shapeshift',
    'Steady Shot',
    'Fireblast',
    'Reinforce',
    'Lesser Heal',
    'Dagger Mastery',
    'Totemic Call',
    'Life Tap',
    'Armor Up!',

    'Dire Shapeshift',
    'Ballista Shot',
    'Fireblast Rank 2',
    'The Silver Hand',
    'Heal',
    'Poisoned Daggers',
    'Totemic Slam',
    'Soul Tap',
    'Tank Up!',

    'Plague Lord',
    'Build-A-Beast',
    'Berserker Throw',
    'Dinomancy',
    'Icy Touch',
    'The Four Horsemen',
    'The Tidal Hand',
    'Voidform',
    'Mind Spike',
    'Mind Shatter',
    'Transmute Spirit',
    'Lightning Jolt',
    'Siphon Life',
    'INFERNO!',
    'Bladestorm',
    'Blast Shield',
    'Delivery Drone',
    'KABOOM!',
    'Micro-Squad',
    'Zap Cannon',
    'DIE, INSECT!'
]

overload_dict = {}

class PlayerInfo:
    def __init__(self):
        self.mana_spent_list = []
        self.hp_count   = 0
        self.card_count = 0

def build_csv(json_file_name, csv_file_name):
    with open(json_file_name, 'r') as f:
        game_info_dict = json.load(f)
    game_list = game_info_dict['games']

    csv_exists = os.path.isfile(csv_file_name)

    with open(csv_file_name, 'a+') as csvfile:
        fieldnames = [
            'id',
            # 'mode',
            'p1_class',
            'p2_class',
            'result',
            'first',
            'p1_hp_count',
            'p2_hp_count',
            'p1_card_count',
            'p2_card_count',
            'p1_floated_mana_05',
            'p2_floated_mana_05',
            'p1_floated_mana_10',
            'p2_floated_mana_10',
            'p1_floated_mana',
            'p2_floated_mana',
            'w_hp_dif',
            'w_card_dif',
            'w_floated_mana_05_dif',
            'w_floated_mana_10_dif',
            'w_floated_mana_dif'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not csv_exists:
            writer.writeheader()
        for game in game_list:
            if game['mode'] == 'arena':
                writer.writerow(get_game_info(game))

def get_game_info(game):
    temp_dict = {
        'id': game['id'],
        # Currently just filter by arena mode
        # 'mode':     game['mode'],
        'p1_class': game['hero'],
        'p2_class': game['opponent'],
        'result':   game['result'],
        'first':    not game['coin']
    }

    p1_info = PlayerInfo()
    p2_info = PlayerInfo()

    for card_info in game['card_history']:
        if card_info['player'] == 'me':
            process_card(card_info, p1_info)
        else:
            process_card(card_info, p2_info)

    p1_fm_05, p1_fm_10, p1_fm = process_mana(p1_info.mana_spent_list)
    p2_fm_05, p2_fm_10, p2_fm = process_mana(p2_info.mana_spent_list)

    if game['result'] == 'win':
        w_fm_05 = p1_fm_05 - p2_fm_05
        w_fm_10 = p1_fm_10 - p2_fm_10
        w_fm    = p1_fm - p2_fm
        w_hp_dif   = p1_info.hp_count - p2_info.hp_count
        w_card_dif = p1_info.card_count - p2_info.card_count
    else:
        w_fm_05 = p2_fm_05 - p1_fm_05
        w_fm_10 = p2_fm_10 - p1_fm_10
        w_fm    = p2_fm - p1_fm
        w_hp_dif   = p2_info.hp_count - p1_info.hp_count
        w_card_dif = p2_info.card_count - p1_info.card_count

    temp_dict['p1_hp_count']           = p1_info.hp_count
    temp_dict['p1_card_count']         = p1_info.card_count
    temp_dict['p2_hp_count']           = p2_info.hp_count
    temp_dict['p2_card_count']         = p2_info.card_count
    temp_dict['p1_floated_mana_10']    = p1_fm_10
    temp_dict['p1_floated_mana']       = p1_fm
    temp_dict['p2_floated_mana_10']    = p2_fm_10
    temp_dict['p2_floated_mana']       = p2_fm
    temp_dict['w_hp_dif']              = w_hp_dif
    temp_dict['w_card_dif']            = w_card_dif
    temp_dict['w_floated_mana_05_dif'] = w_fm_05
    temp_dict['w_floated_mana_10_dif'] = w_fm_10
    temp_dict['w_floated_mana_dif']    = w_fm

    pprint.pprint(temp_dict)

    return temp_dict

def process_card(card_info,player_info):
    turn = card_info['turn']
    name = card_info['card']['name']

    # weird occurences in the data
    # either fix in dataset or notice card name and set cost via lookup table
    if (turn == 0) or (card_info['card']['mana'] is None):
        return
    recorded_turn = len(player_info.mana_spent_list)
    if turn > recorded_turn:
        for i in range(0, turn-recorded_turn):
            player_info.mana_spent_list.append(0)

    try:
        if name != 'The Coin':
            player_info.mana_spent_list[turn-1] += card_info['card']['mana']
        else:
            player_info.mana_spent_list[turn-1] -= 1
    except:
        pprint.pprint(player_info.mana_spent_list)
        pprint.pprint(card_info)
        exit()

    if name in hp_list:
        player_info.hp_count += 1
    elif name != 'The Coin':
        player_info.card_count += 1

def process_mana(mana_spent_list):
    floated_mana_05 = 0
    floated_mana_10 = 0
    floated_mana = 0

    for index, mana_used in enumerate(mana_spent_list):
        mana_available = min(index+1, 10)
        floated_mana_turn = mana_available - mana_used
        # print 'index: ' + str(index)
        # print 'mana available: ' + str(mana_available)
        # print 'mana used: ' + str(mana_used)
        # print 'mana floated: ' + str(floated_mana_turn)

        floated_mana += floated_mana_turn
        if index < 5:
            floated_mana_05 += floated_mana_turn
        if index < 10:
            floated_mana_10 += floated_mana_turn

    return floated_mana_05, floated_mana_10, floated_mana


def main():
    build_csv(sys.argv[1], sys.argv[2])

if __name__== "__main__":
    main()