import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'adventurers.settings'
django.setup()

from missionboard.models import *
from accounts.models import Member
from django.contrib.auth.models import User
from django.utils import timezone

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
    skill_list = ['Python', 'JavaScript', 'C', 'C++', 'C#',
                  'Android', 'iOS', 'Visual Basic', 'Java',
                  'Web Design', 'Ruby', 'Graphic Design', 'Photography']
    for s in skill_list:
        skill = Skill.objects.create(name=s, description='{} 是個好程式'.format(s))
    print("{} skills generated and committed to DB.".format(Skill.objects.count()))


def gen_missions(num):
    counter = 0
    for n in range(0, num):
        gen_missions_helper()
        counter += 1
    print("{} missions generated and committed to DB.".format(counter))


def gen_missions_helper():
    u = None
    while u is None or u is User.objects.get(id=1):
        u = User.objects.get(id=random.randint(1, User.objects.count()))

    worker_num = random.randint(2, 6)
    level = random.randint(1, 11)
    app_date = fake.date_time_between(
        start_date="-14d", end_date="+7d", tzinfo=tz('Asia/Taipei'))

    if app_date > timezone.now():
        status = 'application'
    else:
        status = 'in_progress'

    m = Mission.objects.create(
        name=' '.join(fake.text().split(' ')[:5]),
        posted_by=u,
        posted_on=fake.date_time_between(
            start_date="-30d", end_date="-15d", tzinfo=tz('Asia/Taipei')),
        status=status,
        application_deadline=app_date,
        description=fake.text(),
        working_deadline=fake.date_time_between(
            start_date="+15d", end_date="+30d", tzinfo=tz('Asia/Taipei')),
        required_level=level,
        required_worker_num=worker_num
    )

    skill_list = []
    for n in range(1, random.randint(2, 4)):
        s = Skill.objects.random_pick()
        if s not in skill_list:
            skill_list.append(s)
    m.required_skills.set(skill_list)
    m.save()

    applied_user = []
    num = random.randint(2, 20)
    all_users = list(User.objects.all().exclude(username='AnonymousUser'))

    for x in random.sample(all_users, num):
        ma = MissionApplication.objects.create(applied_by=x, mission=m)
        x.my_profile.missions_wip.add(ma.mission)


if __name__ == '__main__':
    main()
