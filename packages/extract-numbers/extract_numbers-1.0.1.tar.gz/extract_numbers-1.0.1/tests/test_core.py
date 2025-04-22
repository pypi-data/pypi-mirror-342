import pytest
from extract_numbers import ExtractNumbers

def test_extract_numbers():
    extractor = ExtractNumbers()
    text = "Order number 7864657 contains 4 items and costs $567 (£432 or €497)."
    assert extractor.extractNumbers(text) == ["7864657", "4", "567", "432", "497"]

def test_extract_numbers_commas():
    extractor = ExtractNumbers()       
    assert extractor.extractNumbers("100,000 results found out of 100,000,000") == ["100,000", "100,000,000"]        
    assert extractor.extractNumbers("100,000,000,000 is a large amount, and so is 900,000,000,000,000") == ["100,000,000,000", "900,000,000,000,000"]

def test_extract_standardized_numbers_with_commas():
    extractor = ExtractNumbers()       
    assert extractor.extractNumbers("1,000, 100,000, 1,000,000, and 1,234,567,890") == ["1,000", "100,000", "1,000,000", "1,234,567,890"] 
    assert extractor.extractNumbers("1,000.77, 100,000.9, 1,000,000.32, and 1,234,567,890.789") == ["1,000.77", "100,000.9", "1,000,000.32", "1,234,567,890.789"]            

def test_extract_numbers_decimals():
    extractor = ExtractNumbers()  
    assert extractor.extractNumbers("Your rating is 8.7") == ["8.7"]
    assert extractor.extractNumbers("Your score is 7.7/10.0") == ["7.7", "10.0"]
    
def test_extract_numbers_decimals_and_commas():
    extractor = ExtractNumbers()  
    assert extractor.extractNumbers("Your balance: $100,000.77") == ["100,000.77"]
    assert extractor.extractNumbers("Your balance: $100,000.77, previous month: $90,899.89") == ["100,000.77", "90,899.89"]
    assert extractor.extractNumbers("Your balance: 100,000,000.77, previous month: 90,899,232.89") == ["100,000,000.77", "90,899,232.89"]

def test_extract_numbers_negatives():
    extractor = ExtractNumbers()  
    assert extractor.extractNumbers("Temperature: -15") == ["-15"]
    assert extractor.extractNumbers("Temperature: -15°C, yesterday: -22°C") == ["-15", "-22"]

def test_extract_numbers_negative_decimals():
    extractor = ExtractNumbers()  
    assert extractor.extractNumbers("Temperature: -15.7") == ["-15.7"]
    assert extractor.extractNumbers("Temperature: -15.7°C, yesterday: -22.33°C") == ["-15.7", "-22.33"]

def test_extract_numbers_negative_commas():
    extractor = ExtractNumbers()  
    assert extractor.extractNumbers("Can't think of some -150,000 example, but it should work") == ["-150,000"]
    assert extractor.extractNumbers("-170,000, -222,987 and -222,987,899 work too!") == ["-170,000", "-222,987", "-222,987,899"]

def test_extract_numbers_negative_decimals_and_commas():
    extractor = ExtractNumbers()  
    assert extractor.extractNumbers("-170,000.77, -222,987.66 and -222,987,899.29") == ["-170,000.77", "-222,987.66", "-222,987,899.29"]    

def test_extract_numbers_no_number_in_the_string():
    extractor = ExtractNumbers()  
    assert extractor.extractNumbers("No results found for your query!") == []
  
def test_extract_numbers_as_string_false():
    extractor = ExtractNumbers({"as_string": False})  
    assert extractor.extractNumbers("3030 results found") == [3030]
    assert extractor.extractNumbers("100,000 results found") == [100000]
    assert extractor.extractNumbers("Your rating is 7.7/10.0") == [7.7, 10]
    assert extractor.extractNumbers("Your balance: 100,000,000.77, previous month: 90,899,232.89") == [100000000.77, 90899232.89]
    assert extractor.extractNumbers("Temperature: -15, yesterday: -22") == [-15, -22]
    assert extractor.extractNumbers("Temperature: -15.7") == [-15.7]
    assert extractor.extractNumbers("-170,000.77, -222,987.66 and -222,987,899.29") == [-170000.77, -222987.66, -222987899.29]
    assert extractor.extractNumbers("-170,000, -222,987 and -222,987,899") == [-170000, -222987, -222987899]

def test_extract_numbers_remove_commas():
    extractor = ExtractNumbers({"remove_commas": True})  
    assert extractor.extractNumbers("100,000,000 results found!") == ["100000000"]
    assert extractor.extractNumbers("77, 77.77, -9, 300,000") == ["77", "77.77", "-9", "300000"]
    assert extractor.extractNumbers("222,987.66, 77, 77.77, -9, 300,000, and -222,987,899.29") == ["222987.66", "77", "77.77", "-9", "300000", "-222987899.29"]

def test_extract_standardized_numbers_european_format():
    extractor = ExtractNumbers({"european_format": True})       
    assert extractor.extractNumbers("1.000, 100.000, 1.000.000, and 1.234.567.890") == ["1.000", "100.000", "1.000.000", "1.234.567.890"] 
    assert extractor.extractNumbers("1.000,77, 100.000,9, 1.000.000,32, and 1.234.567.890,789") == ["1.000,77", "100.000,9", "1.000.000,32", "1.234.567.890,789"]   
    assert extractor.extractNumbers("Your balance: $100.000,77") == ["100.000,77"] 
    assert extractor.extractNumbers("Your rating is 8,7") == ["8,7"]
    assert extractor.extractNumbers("Your score is 7,7/10,0") == ["7,7", "10,0"]        
    assert extractor.extractNumbers("-170.000,77, -222.987,66 and -222.987.899,29") == ["-170.000,77", "-222.987,66", "-222.987.899,29"]    

def test_extract_remove_commas_with_european_format():
    extractor = ExtractNumbers({"remove_commas": True, "european_format": True})       
    assert extractor.extractNumbers("1.000, 100.000, 1.000.000, and 1.234.567.890") == ["1000", "100000", "1000000", "1234567890"] 
    assert extractor.extractNumbers("1.000,77, 100.000,9, 1.000.000,32, and 1.234.567.890,789") == ["1000,77", "100000,9", "1000000,32", "1234567890,789"] 

def test_extract_as_string_false_with_european_format():
    extractor = ExtractNumbers({"as_string": False, "european_format": True})           
    assert extractor.extractNumbers("1.000, 100.000, 1.000.000, and 1.234.567.890") == [1000, 100000, 1000000, 1234567890] 
    assert extractor.extractNumbers("1.000,77, 100.000,9, 1.000.000,32, and 1.234.567.890,789") == [1000.77, 100000.9, 1000000.32, 1234567890.789] 

    # should behave the same
    extractor = ExtractNumbers({"as_string": False, "remove_commas": True, "european_format": True})     
    print(extractor.extractNumbers("1.000, 100.000, 1.000.000, and 1.234.567.890"))      
    assert extractor.extractNumbers("1.000, 100.000, 1.000.000, and 1.234.567.890") == [1000, 100000, 1000000, 1234567890] 
    assert extractor.extractNumbers("1.000,77, 100.000,9, 1.000.000,32, and 1.234.567.890,789") == [1000.77, 100000.9, 1000000.32, 1234567890.789]               

def test_extract_numbers_invalid_text_argument():
    extractor = ExtractNumbers()
    with pytest.raises(ValueError, match=r"Invalid argument: Expected 'text' to be of type str, but got int."):
        extractor.extractNumbers(12345)
    with pytest.raises(ValueError, match=r"Invalid argument: Expected 'text' to be of type str, but got dict."):
        extractor.extractNumbers(dict({"a": 1}))

def test_extract_numbers_invalid_additional_option():
    with pytest.raises(ValueError, match=r"Invalid option 'additional'\. Expected one of \['as_string', 'remove_commas', 'european_format'\]\."):
        ExtractNumbers({"additional": True})

def test_extract_numbers_invalid_as_string():
    with pytest.raises(TypeError, match="Option 'as_string' must be a boolean."):
        ExtractNumbers({"as_string": 27})

def test_extract_numbers_invalid_remove_commas():
    with pytest.raises(TypeError, match="Option 'remove_commas' must be a boolean."):
        ExtractNumbers({"remove_commas": "yes"})

def test_extract_numbers_invalid_european_format():
    with pytest.raises(TypeError, match="Option 'european_format' must be a boolean."):
        ExtractNumbers({"european_format": "yes"})