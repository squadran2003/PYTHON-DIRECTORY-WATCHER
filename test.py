import unittest
import directories

class directoryTest(unittest.TestCase):

	
	def test_add_directories(self):
		result = " \n Directory added"
		self.assertNotEqual(directories.add_directories("/home/andy/Desktop/PYTHON-DIRECTORY-WATCHER/include","/home/andy/Desktop/PYTHON-DIRECTORY-WATCHER/test.bat",2),result)
		self.assertEqual(directories.add_directories("/home/andy/Desktop/PYTHON-DIRECTORY-WATCHER/include/","/home/andy/Desktop/PYTHON-DIRECTORY-WATCHER/include/test.bat",2),result)


	def test_del_directories(self):
		result = "The directory you are trying to delete does not exist"
		# if there is a record with id 1 i should not get the string result
		self.assertNotEqual(directories.del_directories(2),result)
		
		# if there is a no record with id 45 i should get the result string above  
		self.assertEqual(directories.del_directories(45),result)			                     

if __name__ =="__main__":
	unittest.main()	
	
