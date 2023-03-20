from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem

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
        self.layer = None
        self.invert = False


    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if layer != self.layer:
            self.layer = layer
            return True

        return False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
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
        """
        if self.layer != None:
            self.layer = None
            return True
        return False


    def special(self):
        """
        Special mode. Different for each store implementation.
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
        self.layers = CircularQueue(100)
        

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if self.layers.is_full():
            return False
        else:
            self.layers.append(layer)
            return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        if self.layers.is_empty():
            return start
            
        self.layers2 = CircularQueue(100)

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
        """

        if not self.layers.is_empty():
            self.layers.serve()
            return True 
        else:
            return False

    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        stack = ArrayStack(len(self.layers))
        reversed_layers = CircularQueue(len(self.layers))

        for i in range (len(self.layers)):
            item = self.layers.serve()
            stack.push(item)
            self.layers.append(item)

        while not stack.is_empty():
            reversed_layers.append(stack.pop())

        self.layers = reversed_layers
        



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
        self.layers = ArraySortedList(20)
        self.templayers = ArraySortedList(20)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        self.layers.add(ListItem(layer, layer.index))

        if self.layers.__contains__(ListItem(layer, layer.index)):
            return True
        
        self.templayers.add(ListItem(layer, layer.name))


    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """

        if self.layers.is_empty():
            return start

        
        self.layerstemp = ArraySortedList(20)
        
        for i in range(len(self.layers)):
            item = self.layers[i].value 
            color = item.apply(start, timestamp, x, y)
            start = color
            self.layerstemp.add(self.layers[i])

        self.layers = self.layerstemp

        return color
    

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """

        for i in range(len(self.layers)):
            if self.layers[i].value == layer:
                self.layers.remove(self.layers[i])

        if not self.layers.__contains__(ListItem(layer, layer.index)):
            return True
 

    def special(self):
        """
        Special mode. Different for each store implementation.
        """

        l = len(self.templayers)

        if l % 2 == 1:
            mid = l // 2
        else:
            mid = l // 2 - 1

        self.templayers.remove(self.templayers[mid])

        newtemp = ArraySortedList(20)

        for i in range(len(self.templayers)):
            value = self.templayers[i].value 
            key = value.index 
            newtemp.add(ListItem(value, key))

        self.layers = newtemp

        




    
