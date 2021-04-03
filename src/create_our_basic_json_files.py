import json
from utils import bot_util as utils


def create_watchlist():
    dictionary = {'ev': {'names': ['ev', 'electrical vehicle', 'cars'], 'symbols': ['TSLA', 'NIO', 'XPEV', 'SOLO', 'LI', 'AYRO']},
                  'weeds': {'names': ['weed', 'weeds', 'canopy', 'cannabis', 'marijuana', 'pot', 'pots'],
                            'symbols': ['TLRY', 'APHA', 'CRON', 'CGC', 'ACB', 'HEXO', 'SNDL', 'IGC']},
                  'NFT': {'names': ['nft', 'art'],
                          'symbols': ['TKAT', 'OCG', 'IMTE', 'YVR', 'WKEY', 'HOFV', 'MFH']},
                  '3D': {'names': ['3d', 'threed', 'print', 'printing', '3dprinting', '3d printing'],
                         'symbols': ['PRNT', 'DDD', 'NNDM']},
                  'crypto': {'names': ['crypto', 'btc', 'bitcoin', 'cryptocurrency', 'btc mining'],
                             'symbols': ['RIOT', 'MARA', 'SOS', 'NXTD', 'FTFT', 'BTBT', 'CNET', 'NCTY']},
                  'battery': {'names': ['battery', 'charging', 'clean energy', 'solar', 'chargers'],
                              'symbols': ['FCEL', 'PLUG', 'CBAT']},
                  'oiler': {'names': ['oilers', 'oiler', 'oil'],
                            'symbols': ['XOM', 'GBR', 'USEG', 'PED']},
                  'rare resource': {'names': ['rare resource', 'gold', 'copper', 'nikel', 'precious metal', 'miner', 'mining'],
                                    'symbols': ['NAK', 'GSV', 'CBAT']},
                  'space': {'names': ['space', 'satellite'],
                            'symbols': ['SPCE', 'MAXR', 'IRDM', 'GILT', 'GSAT', 'VISL']},
                  'wsb': {'names': ['wsb'],
                          'symbols': ['GME', 'KOSS', 'EXPR', 'AMC']},
                  'sustainability': {'names': ['sustainability', 'sustainable foods', 'green food', 'alternative meat'],
                                     'symbols': ['BYND', 'TTCF', 'NEXE', 'VRYYF']},
                  'shippers': {'names': ['ship', 'shipper', 'shippers'],
                               'symbols': ['CTRM', 'GLBS', 'SHIP', 'SINO']},
                 }

    json_object = json.dumps(dictionary, indent=4)

    root_dir = utils.get_root_dir()
    with open(root_dir+"/src/Watchlists.json", "w") as outfile:
        outfile.write(json_object)


def create_sympathy_plays():
    # add the ticker to the first entry of the sympathy
    dictionary = {'TSLA': ['TSLA', 'NIO', 'XPEV', 'SOLO', 'LI', 'AYRO'],
                  'NIO': ['XPEV', 'LI'],
                  'TLRY': ['TLRY', 'SNDL', 'APHA', 'CGC', 'ACB', 'HEXO', 'IGC'],
                  'SNDL': ['SNDL', 'TLRY', 'IGC'],
                  'TKAT': ['TKAT', 'OCG', 'IMTE', 'YVR', 'WKEY', 'HOFV', 'MFH'],
                  'HOFV': ['HOFV', 'TKAT', 'OCG', 'IMTE', 'YVR', 'WKEY', 'MFH'],
                  'WKEY': ['WKEY', 'TKAT', 'OCG', 'IMTE', 'YVR', 'HOFV', 'MFH'],
                  'PRNT': ['PRNT', 'DDD', 'NNDM'],
                  'DDD': ['DDD', 'NNDM', 'PRNT'],
                  'NNDM': ['NNDM', 'DDD', 'PRNT'],
                  'RIOT': ['RIOT', 'MARA', 'SOS', 'NXTD', 'FTFT', 'BTBT', 'CNET', 'NCTY'],
                  'MARA': ['MARA', 'RIOT', 'SOS', 'NXTD', 'FTFT', 'BTBT', 'CNET', 'NCTY'],
                  'SOS': ['SOS', 'RIOT', 'MARA', 'NXTD', 'FTFT', 'BTBT', 'CNET', 'NCTY'],
                  'FCEL': ['FCEL', 'PLUG', 'CBAT'],
                  'PLUG': ['PLUG', 'FCEL', 'CBAT'],
                  'SPCE': ['SPCE', 'MAXR', 'IRDM', 'GILT'],
                  'MAXR': ['MAXR', 'SPCE', 'IRDM', 'GILT'],
                  'IRDM': ['IRDM', 'SPCE', 'MAXR', 'GILT'],
                  'GILT': ['GILT', 'SPCE', 'MAXR', 'IRDM'],
                  'GME': ['GME', 'KOSS', 'EXPR', 'AMC'],
                  'KOSS': ['KOSS', 'GME', 'EXPR', 'AMC'],
                  'EXPR': ['EXPR', 'GME', 'KOSS', 'AMC'],
                  'AMC': ['AMC', 'GME', 'KOSS', 'EXPR'],
                  'BYND': ['BYND', 'TTCF'],
                  'TTCF': ['TTCF', 'BYND'],
                  'CTRM': ['CTRM', 'GLBS', 'SHIP'],
                  'GLBS': ['GLBS', 'CTRM', 'SHIP'],
                  'SHIP': ['SHIP', 'CTRM', 'GLBS'],
                  }

    json_object = json.dumps(dictionary, indent=4)

    root_dir = utils.get_root_dir()
    with open(root_dir+"/src/Sympathy_plays.json", "w") as outfile:
        outfile.write(json_object)


