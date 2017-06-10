import django
import os

os.environ['DJANGO_SETTINGS_MODULE']='adventurers.settings'
django.setup()

from missionboard.models import *
from accounts.models import Member
from django.contrib.auth.models import User

import random
from faker import Factory
fake = Factory.create()

def main():
    gen_skills()
    gen_missions(50)
    gen_users(10)


    print('\nDone!')


def gen_users(num):
    for n in range(0, num):
        u = User.objects.create(username=fake.name().replace(' ','_').lower())
        u.set_password('P@ssw0rd')
        u.save()

        m = Member.objects.create(user=u,
                              level=random.randint(1,6),
                              bios=fake.text(),
                              contact=fake.text())
        skill_list = []
        for x in range(1, random.randint(1,3)):
            skill_list.append(Skill.objects.random_pick())
        m.skills.set(skill_list)
        m.save()


    print("{} users generated and committed to DB.".format(User.objects.count()))


def gen_skills():
    skill_list = ['Python', 'JavaScript', 'C', 'C++', 'C#', 'Android', 'iOS', 'Visual Basic', 'Java']
    for s in skill_list:
        skill = Skill.objects.create(name=s, description='{} 是個好程式'.format(s))

    print("{} skills generated and committed to DB.".format(Skill.objects.count()))


def gen_missions(num):
    for n in range(0, num):
        Mission.objects.generate()
    print("{} missions generated and committed to DB.".format(Mission.objects.count()))


if __name__ == '__main__':
    main()
