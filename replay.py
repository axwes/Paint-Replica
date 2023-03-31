from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue
from action import PaintAction

class ReplayTracker:

    action_queue = CircularQueue(1000)
    replay_queue = CircularQueue(1000)
    replaying = False


    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.

        Time complexity: 
            Best case: O(1)
            Worse case: O(1)
        """
        self.replaying = True 

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.

        Args:
            action (PaintAction): The paint action to store for replaying.
            is_undo (bool, optional): Indicates if the action is an undo action or not.
                                      For Special, Redo, and Draw actions, this is False. Defaults to False.

        Time complexity: 
            Best case: O(1)
            Worse case: O(1)
        """
        self.action_queue.append((action, is_undo))


    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.

        Args:
            grid (Grid): The grid where the replay action will be performed.

        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Time complexity: 
            Best case: O(1) - if not in replaying mode or if the replay is finished
            Worst case: O(n) - where n is the number of steps in the PaintAction.steps list
        """
        if self.replaying:
            if self.replay_queue.is_empty() and self.action_queue.is_empty():
                self.replaying = False
                return True

            if self.replay_queue.is_empty(): # if replay queue is empty but action queue is not
                self.replay_queue = self.action_queue
                self.action_queue = CircularQueue(1000) #reset action queue so new action can be added 

            action, is_undo = self.replay_queue.serve()
            if action is None:  
                return True  # Return True to indicate the replay is finished
            if is_undo:
                action.undo_apply(grid)
            else:
                action.redo_apply(grid)
            return False
        else:
            return True




if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

