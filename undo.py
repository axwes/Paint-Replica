from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    undo_array = ArrayStack(100000)
    redo_array = ArrayStack(100000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.

        Args:
            action (PaintAction): The paint action to be stored in self.undo_array
        
        Time complexity: 
            Best case: O(1)
            Worse case: O(1)
        """
        self.undo_array.push(action)

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

         Args:
            grid (Grid): The grid to which the undone action is applied.

        :return: The action that was undone, or None.

        Time complexity: 
            Best case: O(1) - if the undo_array is empty
            Worst case: O(n) -  where n is the number of steps in the PaintAction.steps list
        """
        if self.undo_array.is_empty():
            return None 
        undoItem = self.undo_array.pop()
        undoItem.undo_apply(grid)
        self.redo_array.push(undoItem)

        return undoItem

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        Args:
            grid (Grid): The grid to which the redone action is applied.

        :return: The action that was redone, or None.

        Time complexity:
            Best case: O(1) - if the redo_array is empty
            Worst case: O(n) - where n is the number of steps in the PaintAction.steps list
        """
        if self.redo_array.is_empty():
            return None 
        
        redoItem = self.redo_array.pop()
        redoItem.redo_apply(grid)
        
        return redoItem
