from reflect import *
from reflect.dialog import *


def csv_to_jagged_tsv(path='Laura_2025-03-21_09-32.csv'):
    """ Convert a conversation log (CSV) into the jagged tilde-separated values format of dialog.py """
    # d = {f.name: pd.read_csv(f) for f in DATA_DIR.glob('*.csv')}
    path = Path(path)
    if not path.is_file():
        path = DATA_DIR / path
    df = pd.read_csv(path)
    # table = list(['~'.join(list(x)) for x in df['role text'.split()].values])
    dt = pd.concat(
        [df[df.role == role]['text'].reset_index() for role in 'counselor client'.split()],
        axis=1, ignore_index=True)
    dt = dt.drop(labels=[0, 2], axis=1)
    dt.columns = 'counselor client'.split()
    dt['npc'] = 1
    dt['node_id'] = dt.index.values + 101
    dt['dest_id'] = dt['node_id'] + 1
    dt['counselor_response'] = list(dt['counselor'][1:]) + ['']
    # dt['client counselor_response'.split()].to_csv(DATA_DIR / 'Laura_response_pairs.csv')

    # this is only possible because there is only one possible response for every prompt in a log file
    dt = dt['npc node_id client counselor_response'.split()].copy()
    dt.to_csv(path.with_suffix('.jtsv'), sep='~', header=False)
    return dt
