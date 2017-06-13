import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'adventurers.settings'
django.setup()

from missionboard.models import *
from accounts.models import Member
from django.contrib.auth.models import User

import random
from faker import Factory
fake = Factory.create()


def main():
    print("\nGenerating data ...")
    gen_skills()
    gen_users(50)
    gen_missions(100)
    print('Done!')


def gen_users(num):
    counter = 0
    for n in range(0, num):
        name = fake.name().replace(' ', '_').lower()
        u = User.objects.create(username=name,
                                email='{}@fake.test.local'.format(name))
        u.set_password('P@ssw0rd')
        u.save()

        m = Member.objects.create(user=u,
                              level=random.randint(1, 20),
                              bios=fake.text(),
                              contact=fake.text())
        skill_list = []
        for x in range(1, random.randint(1, 3)):
            skill_list.append(Skill.objects.random_pick())
        m.skills.set(skill_list)
        m.missions_wip.set([])
        m.missions_completed.set([])
        m.missions_failed.set([])
        m.save()
        counter += 1

    print("{} users generated and committed to DB.".format(counter))


def gen_skills():
    skill_list=['Python', 'JavaScript', 'C', 'C++', 'C#',
                'Android', 'iOS', 'Visual Basic', 'Java',
                'Web Design', 'Ruby', 'Graphic Design', 'Photography']
    for s in skill_list:
        skill=Skill.objects.create(name=s, description='{} 是個好程式'.format(s))
    print("{} skills generated and committed to DB.".format(Skill.objects.count()))


def gen_missions(num):
    counter=0
    for n in range(0, num):
        Mission.objects.generate()
        counter += 1
    print("{} missions generated and committed to DB.".format(counter))


if __name__ == '__main__':
    main()
