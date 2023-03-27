from __future__ import annotations
from abc import ABC, abstractmethod
from layers import black
from layer_util import Layer, get_layers
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.bset import BSet
class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        '''
        Time complexity: O(1)
        '''
        self.layer = None  # Initialize layer variable with None
        self.invert = False # Initialize invert variable with False


    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        Time complexity: O(1)
        """
        if layer != self.layer:
            self.layer = layer # Set the layer 
            return True

        return False 
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Time complexity: O(1)
        """

        #check if there's layer, if no layer then just return the start color 
        if self.layer is None:
            return start
        
        #if there's layer, apply the layer to the start color and store it in color 
        color = self.layer.apply(start, timestamp, x, y) # self.layer.apply will return a tuple of 3 int after applying the layer to the start color 

        #because we can't iterate through Layer, we can use the tuple returned in self.layer.apply to invert the color in this function
        if self.invert == True:
            color = tuple(255 - c for c in color)

        return color
        
        
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        Time complexity: O(1)
        """
        if self.layer != None:
            self.layer = None # Set the layer to None
            return True
        return False 


    def special(self):
        """
        Special mode. Different for each store implementation.
        Time complexity: O(1)
        """
        self.invert = not self.invert
        

        

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    def __init__(self):
        """
        Time complexity: O(1) [because the circular queue is initalised with 20 so its no longer O(n)]
        """
        self.layers = CircularQueue(20)
        self.layers2 = CircularQueue(20)
        

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        Time complexity: O(1)
        """
        if self.layers.is_full():
            return False
        else:
            self.layers.append(layer)
            return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Time complexity: O(n) where n is the number of layers in the store 
        """
        if self.layers.is_empty():
            return start

        for _ in range(len(self.layers)):
            item = self.layers.serve()
            colors = item.apply(start , timestamp, x, y)
            start = colors
            self.layers2.append(item)

        self.layers = self.layers2

            
        return colors


    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        Erasing from an Additive Layer always removes the oldest remaining layer
        Time complexity: O(1)
        """

        if not self.layers.is_empty():
            self.layers.serve()
            return True 
        else:
            return False

    def special(self):
        """
        Special mode. Different for each store implementation.
        Reverses the "ages" of each layer, so the oldest layer is now the youngest layer, and so on.
        Time complexity: O(n) where n is the number of layers in the store
        """
        stack = ArrayStack(len(self.layers))
        reversed_queue = CircularQueue(len(self.layers))

        while not self.layers.is_empty():
            layer = self.layers.serve()
            stack.push(layer)

        while not stack.is_empty():
            reversed_queue.append(stack.pop())

        self.layers = reversed_queue
        

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    def __init__(self) -> None:
        '''
        Initializes the SequenceLayerStore with a BSet object and an ArraySortedList object.
        Time complexity: O(1)
        '''
        self.layers = BSet(1)
        self.layers_array = ArraySortedList(20)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        Time complexity:
            - Best-case: O(1), if the layer is already in the store.
            - Worst-case: O(n), if the layer is not in the store and need to be added in.
        """
        if not self.layers.__contains__(layer.index + 1):
            self.layers.add(layer.index + 1)
            self.layers_array.add(ListItem(layer, layer.name))
            return True
        return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Time complexity: O(n), where n is the number of layers in the store.
        """

        if self.layers.is_empty():
            color = start 

        registered_layers = get_layers()
        
        for i in range(1, len(registered_layers)):
            if i in self.layers:
                layers = registered_layers[i-1]
                color = layers.apply(start, timestamp, x, y)
                start = color

        return color
    

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
         Time complexity:
            - Best-case: O(1), if the layer is not in the store.
            - Worst-case: O(n), if the layer is in the store and needs to be removed.
        """

        if self.layers.__contains__(layer.index + 1):
            self.layers.remove(layer.index + 1)
            self.layers_array.remove(ListItem(layer, layer.name))
            return True
        return False
 

    def special(self):
        """
        Special mode. Different for each store implementation.
        Removes the median layer from the store based on alphabetical order.
        If there are two median layers, remove the lexicographically smaller one.
        Time complexity: O(n), where n is the number of layers in the store.
        """
        length = len(self.layers_array)

        if length % 2 == 1:
            mid = length // 2
        else:
            mid = length // 2 - 1

        self.layers_array.remove(self.layers_array[mid])

        temp_bset = BSet(1)

        for i in range(len(self.layers_array)):
            temp_bset.add(self.layers_array[i].value.index  + 1)

        self.layers = temp_bset 

        




    
