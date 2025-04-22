from clicknium.common.models.sapitem import SapStatusBarInfo
from clicknium.core.models.uielement import UiElement
from clicknium.core.service.invokerservice import _ExceptionHandle

class SapElement(UiElement):

    def __init__(self, element):
        super(SapElement, self).__init__(element)

    @property
    @_ExceptionHandle.try_except
    def parent(self):
        """
            Get parent element.
                                
            Returns:
                SapElement object if it was found, or None if not
        """
        if self._element.Parent:
            return SapElement(self._element.Parent)
        return None

    @property
    @_ExceptionHandle.try_except
    def children(self):
        """
            Get element's child elements.
                                
            Returns:
                list of SapElement object, a list with elements if any was found or an empty list if not
        """
        child_list = []
        if self._element.Children:            
            for child in self._element.Children:
                child_list.append(SapElement(child))
        return child_list

    @property
    @_ExceptionHandle.try_except
    def next_sibling(self):
        """
            Get next sibling element.
                                
            Returns:
                SapElement object if it was found, or None if not
        """
        if self._element.NextSibling:
            return SapElement(self._element.NextSibling)
        return None

    @property
    @_ExceptionHandle.try_except
    def previous_sibling(self):
        """
            Get previous sibling element.
                                
            Returns:
                SapElement object if it was found, or None if not
        """
        if self._element.PreviousSibling:
            return SapElement(self._element.PreviousSibling)
        return None
    
    @_ExceptionHandle.try_except
    def child(self, index: int):
        """
            Get child element by index.

            Parameters:
                index[Required]: zero-based index. 
                                
            Returns:
                SapElement object if it was found, or None if not
        """
        child_element = self._element.Child(index)
        if child_element:
            return SapElement(self._element.Child(index))
        return None

    @_ExceptionHandle.try_except
    def call_transaction(
        self,
        transaction_code: str,
        timeout: int = 30
    ) -> None:
        """
            Call sap transaction.
 
            Parameters:

                transaction_code[Required]: transaction code string

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        self._element.CallTransaction(transaction_code, timeout * 1000)        

    @_ExceptionHandle.try_except
    def select_item(
        self,
        item: str,
        timeout: int = 30
    ) -> None:
        """
            Select sap item.
 
            Parameters:

                item[Required]: item to be selected

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        self._element.SelectItem(str(item), timeout * 1000)

    @_ExceptionHandle.try_except
    def get_statusbar(
        self, 
        timeout: int = 30
    ) -> SapStatusBarInfo:
        """
            Get sap status bar info.
 
            Parameters:
                timeout: timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                SapStatusBarInfo object.
        """
        statusbar_info = self._element.ReadStatusBar(timeout * 1000)
        return SapStatusBarInfo(statusbar_info)