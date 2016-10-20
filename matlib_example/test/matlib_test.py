"""
Created on Thu Oct 20 11:03:15 2016

@author: neliel
"""

import mathlib
import pytest

class TestFibo(object):
    def setup_method(self, _):
        self._fibo = mathlib.fibo

    def teardown_method(self, _):
        mathlib.fibo =self._fibo
    
    def test_fibo(self):
        assert mathlib.fibo(1) == 1
        assert mathlib.fibo(2) == 1
    
    @pytest.mark.parametrize(("n, result"), [
        (3,2),
        (4,3),
        (5,5),
        (6,8),
        (7,13),
     ])    
     
    def test_fibo_success(self, n, result):
        assert mathlib.fibo(n) == result
    
    def test_fibo_zero(self):
        assert mathlib.fibo(0) == 0
        
 #   def test_fibo_negative(self):
 #       with pytest.raises(ValueError):
 #           mathlib.fibo(-1)
     
    def test_fibo_invalid(self):
        with pytest.raises(TypeError):
            mathlib.fibo("haha")
            
    @pytest.mark.slow
    
    def test_fibo_large(self):
        assert mathlib.fibo(30) == 832040 