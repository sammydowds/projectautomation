from django.test import TestCase
from projects.models import Project
from django.contrib.auth.models import User
from datetime import datetime,date, timedelta

# Create your tests here.
class ProjectTestCase(TestCase):
    def setUp(self):

        # self.user = User.objects.create_user(username='testuser', password='12345')


        Project.objects.create(\
        projectnumber = 200000, \
        projectname = 'Test1', \
        engineering_start=datetime(2018, 12, 31), \
        Mechanical_Release=datetime(2019, 1, 31), \
        Electrical_Release=datetime(2019, 2, 15), \
        Manufacturing=datetime(2019, 3, 31), \
        Finishing=datetime(2019, 4, 20), \
        Assembly=datetime(2019, 5, 20), \
        Integration=datetime(2019, 6, 20), \
        Internal_Runoff=datetime(2019, 7, 20), \
        Customer_Runoff=datetime(2019, 8, 20), \
        Ship=datetime(2019, 9, 20),\
        Install_Start=datetime(2019, 10, 20),\
        Install_Finish=datetime(2019, 11, 20),\
        Documentation=datetime(2019, 12, 20),)

        Project.objects.create(\
        projectnumber = 200001, \
        projectname = 'Test2', \
        engineering_start=None, \
        Mechanical_Release=None, \
        Electrical_Release=None, \
        Manufacturing=None, \
        Finishing=None, \
        Assembly=None, \
        Integration=None, \
        Internal_Runoff=None, \
        Customer_Runoff=None, \
        Ship=None,\
        Install_Start=None,\
        Install_Finish=None,\
        Documentation=None,)

        Project.objects.create(\
        projectnumber = 200002, \
        projectname = 'Test3', \
        engineering_start=datetime(2018, 12, 31), \
        Mechanical_Release=datetime(2019, 1, 31), \
        Electrical_Release=datetime(2019, 2, 15), \
        Manufacturing=datetime(2019, 3, 31), \
        Finishing=datetime(2019, 4, 20), \
        Assembly=datetime(2019, 5, 20), \
        Integration=None, \
        Internal_Runoff=None, \
        Customer_Runoff=None, \
        Ship=None,\
        Install_Start=None,\
        Install_Finish=None,\
        Documentation=None,)





    def test_milestones(self):
        test_proj = Project.objects.get(projectnumber=200000)
        # self.assertEqual(test_proj.engineering_start, datetime(2018, 12, 31))
        milestones_test = test_proj.milestones()
        self.assertEqual(milestones_test['Finishing']['end'], date(2019, 4, 20))
        self.assertNotEqual(milestones_test['Mechanical_Release']['duration'], 31)

        #testing with no dates
        test_proj2 = Project.objects.get(projectnumber=200001)
        milestones_test2 = test_proj2.milestones()
        self.assertEqual(milestones_test2['Finishing']['end'], None)
        self.assertNotEqual(milestones_test2['Mechanical_Release']['duration'], None)

        #testing with no dates
        test_proj3 = Project.objects.get(projectnumber=200002)
        milestones_test3 = test_proj3.milestones()
        self.assertEqual(milestones_test3['Finishing']['end'], date(2019, 4, 20))
        self.assertNotEqual(milestones_test3['Mechanical_Release']['duration'], 31)

    def test_phases(self):
        test_proj = Project.objects.get(projectnumber=200000)
        phase_test = test_proj.phases()
        self.assertEqual(phase_test['Engineering']['end'], date(2019, 2, 15))

        #testing with no Dates
        test_proj2 = Project.objects.get(projectnumber=200001)
        phase_test2 = test_proj2.phases()
        self.assertEqual(phase_test2['Engineering']['end'], None)

        #testing with partial Dates
        test_proj3 = Project.objects.get(projectnumber=200002)
        phase_test3 = test_proj3.phases()
        self.assertEqual(phase_test3['Engineering']['end'], date(2019, 2, 15))

    def test_suggested_tasks(self):
        test_proj = Project.objects.get(projectnumber=200000)
        suggested_tasks = test_proj.suggested_tasks()
        self.assertEqual(suggested_tasks['Order Robot']['start'], test_proj.Assembly - timedelta(weeks=6) )

        #testing no dates entered for the reference milestone
        test_proj2 = Project.objects.get(projectnumber=200001)
        suggested_tasks2 = test_proj2.suggested_tasks()
        self.assertEqual(suggested_tasks2['Order Robot']['start'], None)

        #testing no dates entered for the reference milestone
        test_proj3 = Project.objects.get(projectnumber=200002)
        suggested_tasks3 = test_proj3.suggested_tasks()
        self.assertEqual(suggested_tasks3['Order Robot']['start'], date(2019, 5, 20) - timedelta(weeks=6))

    def test_current_milestone(self):
        #testing as normal with all dates enteredå
        test_proj = Project.objects.get(projectnumber=200000)
        current_milestone = test_proj.current_milestone()
        self.assertEqual(current_milestone['start'], date(2019, 4, 20))

        #testing if no dates are entered
        test_proj2 = Project.objects.get(projectnumber=200001)
        current_milestone2 = test_proj2.current_milestone()
        self.assertEqual(current_milestone2['start'], None)

        #testing if partial dates are entered
        test_proj3 = Project.objects.get(projectnumber=200002)
        current_milestone3 = test_proj3.current_milestone()
        self.assertEqual(current_milestone3['start'], date(2019, 4, 20))

    def test_current_phase(self):
        test_proj = Project.objects.get(projectnumber=200000)
        current_phase = test_proj.current_phase()
        self.assertEqual(current_phase['current_phase'], 'Assembly')

        #testing no dates entered
        test_proj2 = Project.objects.get(projectnumber=200001)
        current_phase2 = test_proj2.current_phase()
        self.assertEqual(current_phase2['current_phase'], None)

        #testing partial dates entered
        test_proj3 = Project.objects.get(projectnumber=200002)
        current_phase3 = test_proj3.current_phase()
        self.assertEqual(current_phase3['current_phase'], 'Assembly')
