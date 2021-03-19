class Meas:
    meas_list = []

    def __init__(self, measurement):
        self.number = measurement[0]

        self.dis = float(measurement[1])
        self.h = float(measurement[2])  # horizontal
        self.v = float(measurement[3])  # vertical
        self.error = float(measurement[4])
        self.meas_list.append(self)

    def __str__(self):
        return self.number


class MeasList:

    def __init__(self, meas_list, another, c):
        self.m_l = meas_list
        self.another = another
        self.c = c

        self.m_dis = (0, 0)
        self.m_h = (0, 0)
        self.m_v = (0, 0)

    def main_loop(self):
        output0 = []
        output1 = []

        r_dis, r_h, r_v = self.round_number()

        for i in range(0, self.c - 1, 2):
            m1, m2 = self.m_l[i], self.m_l[i + 1]

            if not self.bug_detector(i, m1, m2):
                return False

            self.m_dis = self.mean_dis(m1.dis, m2.dis, r_dis)
            self.m_h = self.mean_h(m1.h, m2.h, r_h)
            self.m_v = self.mean_v(m1.v, m2.v, r_v)

            output0.append(self.joining(self.m_l[i], 0))
            output1.append(self.joining(self.m_l[i], 1))

        self.saving(output0, 'srednie')
        self.saving(output1, 'roznice')

        print('Wszystko się udało :)')

    def bug_detector(self, i, m1, m2):
        if m1.error != 0 or m2.error != 0:
            print('punkty {} i {} mają złe wartości w ostatniej kolumie. '
                  'Wynoszą one odpowiednio {} i {}'.format(m1, m2, m1.error, m2.error))
            return False
        if str(m1) != str(m2):
            print('punkt {} nie ma punktu odpowiadającego'.format(m1))
            return False
        if self.c - 1 - i > 1 and m2 == self.m_l[i + 2]:
            print('co najmniej trzy takie same wartości. Mowa o punktach {}'.format(m2))
            return False
        return True

    def round_number(self):
        dis = len(str(self.m_l[0].dis).split('.')[1])
        h = len(str(self.m_l[0].h).split('.')[1])
        v = len(str(self.m_l[0].v).split('.')[1])
        return dis, h, v

    def joining(self, number, n):
        joined_meas = ' '.join((str(number), str(self.m_dis[n]), str(self.m_h[n]), str(self.m_v[n])))
        return joined_meas

    def saving(self, output, text):
        with open('output_{}.txt'.format(text), 'w') as file:
            for a in self.another:
                file.write(a[0])
                file.write('\n')
            for i in range(int(self.c/2)):
                file.write(output[i])
                file.write('\n')

    @staticmethod
    def mean_dis(d1, d2, r):
        mean = round((d1 + d2) / 2, r)

        diff = abs(d1 - d2)

        return round(mean, r), round(diff, r)

    @staticmethod
    def mean_h(h1, h2, r):
        if h1 < h2:
            h1 += 400
        h2 += 200
        mean = (h1 + h2)/2

        if mean >= 400:
            mean -= 400

        diff = abs(h1 - h2)

        return round(mean, r), round(diff, r)

    @staticmethod
    def mean_v(v1, v2, r):
        mean = (v1 - v2 + 400)/2

        diff = abs(400 - (v1 + v2))

        return round(mean, r), round(diff, r)


def import_meas():
    another = []
    counter = 0
    with open('pomiary.txt') as file:
        for line in file:
            meas = line.replace('\n', '').split(' ')
            while '' in meas:
                meas.remove('')
            if len(meas) == 5:
                counter += 1
                Meas(meas)
            else:
                another.append(meas)
        return another, counter


def run():
    another, c = import_meas()
    m = MeasList(Meas.meas_list, another, c)
    m.main_loop()


run()
