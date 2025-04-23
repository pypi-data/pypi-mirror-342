# Refactored from: https://github.com/obxfisherman/dialog_tree/blob/master/dialog.py
from pathlib import Path
import logging
import pdb  # noqa

log = logging.getLogger(__name__)

END_NODE_ID = 999
EXIT_COMMANDS = 'x exit quit'.split()
DATA_FILE = 'dialog.txt'


def describe(dialog_engine=DATA_FILE, npc=1, quiet=False):
    """ Display a table with all of the dialog turns and state transitions for a particular NPC

    >>> describe(quiet=True)
    'Dialog Plan (DialogEngine) rules:...'
    """
    if not isinstance(dialog_engine, DialogEngine):
        dialog_engine = DialogEngine(dialog_engine)
    text = ''
    text += 'Dialog Plan (DialogEngine rules):\n'
    for turn in dialog_engine.turns:
        if turn.npc == npc:
            text += f'NPC:{turn.npc:2} ID:{turn.node_id:3} MSG: {turn.prompt}\n'
            for response in turn.responses:
                text += f'      {response[1]:3} -> {response[0]}\n'
    if not quiet:
        print(text)
    return text


class DialogTurn:
    def __init__(self, npc_id=1, turn_id=1, prompt='Ready?', responses=[('yes', 2), ('no', 1), ('exit', 999)]):
        """ A dialog tree layer with a machine (NPC) prompt and acceptable human "player" responses

        >>> DialogTurn(1,2,'What comes after 1, 2, ?', responses=[('3', 999), ('4',2), ('four', 999)])
        <reflect.dialog.DialogTurn at ...>
        """
        self.prompt = str(prompt)
        self.npc = int(npc_id)
        self.node_id = int(turn_id)
        # make this a dict
        self.responses = []

    def __str__(self):
        text = f'{self.npc:2} {self.node_id:3} {self.prompt}:' + '\n'
        for r in self.responses:
            text += f'    {r[0]} -> {r[1]}' + '\n'
        return text

    def __repr__(self):
        text = f'{self.npc}~{self.node_id}~{self.prompt}~'
        text += "~".join([f'{r[0]}~{r[1]}' for r in self.responses])
        return text

    def __len__(self):
        return len(self.responses)


class DialogEngine:
    """ Conversation manager that implements the conversation plan rules (dialog tree or flow chart transitions)"""

    def __init__(self, path=DATA_FILE, npc=1, node_id=100):
        """ A dialog engine instance can maintain multiple simultaneous NPC personalities

        Inputs:
          path (str): default='dlane.txt' - path to text file containing tilde-separated edge lists: utterance~dest_node_ID
          npc (int): default=1 - starting personality or NPC character ID
          node_id (int): default=100 - start node the conversation (first NPC prompt)
        """
        # FIXME: Each NPC should have its own DialogEngine
        self.npc = npc
        self.node_id = node_id
        self.path = Path(path)
        if not self.path.is_file():
            self.path = Path(__file__).parent / self.path
        assert self.path.is_file(), f"File not found: {self.path}"
        # TODO: make this a dict of dicts named 'turns' or 'layers'
        self.turns = []
        self.load_dialog_file(self.path)

    def __str__(self):
        return describe(self, quiet=True)

    def __repr__(self):
        return '\n'.join([repr(t) for t in self.turns])

    def __len__(self):
        return len(self.turns)

    def size(self):
        # TODO: use sz = Counter([t.npc for t in self.turns])
        npcs = set([t.npc for t in self.turns])
        log.warning(npcs)
        stats = dict(zip(list(npcs), [[]] * len(npcs)))
        for t in self.turns:
            stats[t.npc] += [len(t.responses)]
        # for i in sz:
        #     stats[i] = sum(stats[i])
        # averesps = sum([sz[i] / len(e.turns) for i in npcs]) / len(npcs)
        return len(stats), len(self.turns) / len(stats), sum([sum(stats[i]) / len(stats[i])])

    def load_dialog_file(self, path=None):
        if path is not None:
            self.path = Path(path)
            assert self.path.is_file(), f"File not found: {self.path}"
        with self.path.open() as fin:
            data = fin.read().split('\n')
        for i, row in enumerate(data):
            # GRAMMAR: skip comments and empty lines
            if not row:
                continue
            if row[0] == '#' or not row.strip():
                log.warning(f'Skip comment on line {i}: "{row[:10]}..."')
                continue
            # GRAMMAR: keywords.append(Token('~'))
            # ?row: NPC_ID '~' TURN_ID ~ PROMPT ~ ANS_TEXT ~ ANS_DEST_NODE_ID ~ ...
            row = row.split('~')
            dlg = DialogTurn(int(row[0]), int(row[1]), row[2])
            dlg.responses = [
                (text, int(dest_id)) for (text, dest_id) in zip(row[3:-1:2], row[4::2])
            ]
            log.warning(f'Line {i:03d} contained node {dlg.npc}~{dlg.node_id} with {len(dlg.responses)} possible responses.')
            self.turns.append(dlg)
        log.warning('load_dialog_file: {} lines loaded'.format(len(self.turns)))

    def get_dialog(self, npc=None, node_id=100):
        """ Find dialog node (layer of branches), print it's prompt, and return it

        Each node has a .responses attribute with a list of possible user menu/action choices or commands
        """

        if npc is not None:
            self.npc = npc
        if node_id is not None:
            self.previous_node = self.node_id
            self.node_id = node_id
        # FIXME: replace for loop with dict.get()
        print(self.npc, self.node_id)
        for turn in self.turns:
            if turn.npc == self.npc and turn.node_id == self.node_id:
                return turn

    def talk_to(self, *args, **kwargs):
        """ Find dialog node (layer of branches), print it's prompt, and return it

        Each node has a .responses attribute with a list of possible user menu/action choices or commands
        """
        # pdb.set_trace()
        node = self.get_dialog(*args, **kwargs)
        if node is not None:
            log.debug(f'talk_to(*{args}, **{kwargs}) => {node}')
            print(f'{node.prompt}')
            return node
        else:
            # FIXME: for some reason, even when node is not None, no prompt is printed and else is triggered
            # pdb.set_trace()
            log.error(f"talk_to can't find NPC:{self.npc} node:{self.node_id}")


if __name__ == '__main__':
    engine = DialogEngine(npc=1)
    current_node = engine.talk_to(npc=1, node_id=100)
    # node_id of 0 or END_NODE_ID will abruptly end the game!
    while current_node and current_node.node_id != END_NODE_ID and current_node.responses:
        choices = []
        for i, response in enumerate(current_node.responses):
            choices.append(f'{i:2} - {response[0]}')
        print('\n'.join(choices))
        choice = input('> ')
        if choice.strip():
            choice = choice.lower().strip()
            next_node = None
            if choice in EXIT_COMMANDS:
                current_node = engine.talk_to(npc=1, node_id=END_NODE_ID)
                break
            else:
                for c in enumerate(choices):
                    if choice in c.lower():
                        current_node = engine.talk_to(npc=1, node_id=current_node.responses[i][1])
                        break
    print('GAME OVER')
