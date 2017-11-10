#!/usr/bin/env python
# -*- coding:utf-8 -*-


def draw():
    """pandas dataframe 绘图后写入 html"""
    end_datetime = datetime.datetime.now()
    beg_datetime = end_datetime - datetime.timedelta(days=30)
    daily_video_member_list = DailyVideoMemberReportDAO.get_by_date_range(
        beg_datetime.date(), end_datetime.date()
    )
    df = pd.DataFrame(daily_video_member_list)
    df['date'] = df['date'].apply(lambda date_obj: date_obj.strftime('%m-%d'))
    df = df[[
        'date', 'publish_success_member_num', 'publish_answer_member_num',
        'publish_article_member_num', 'publish_pin_member_num'
    ]]
    df.rename(
        columns={
            'date': 'Date',
            'publish_success_member_num': 'Member Number',
            'publish_answer_member_num': 'Answer Member Number',
            'publish_article_member_num': 'Article Member Number',
            'publish_pin_member_num': 'Pin Member Number',
        },
        inplace=True
    )
    df.set_index('Date', inplace=True)
    df.plot(legend=1)
    plot = df.plot(legend=1)
    fig = plot.get_figure()
    io = StringIO()
    fig.savefig(io, format='png')
    img_data = base64.encodestring(io.getvalue())
    return u'<img src="data:image/png;base64,{}" />'.format(img_data)

if __name__ == '__main__':
    pass
