"""
分页组件
"""


class Pagination(object):
    def __init__(self, current_page, all_count, base_url, query_params, per_page=30, pager_page_count=11):
        """
        分页初始化

        :param current_page: 当前页码
        :param per_page: 每页显示数据条数
        :param all_count: 数据库中总条数
        :param base_url: 基础URL
        :param query_params: QueryDict对象，内部含所有当前URL的原条件
        :param pager_page_count: 页面上最多显示的页码数量
        """
        self.base_url = base_url
        try:
            self.current_page = int(current_page)
            if self.current_page <= 0:
                raise Exception()
        except Exception as e:
            self.current_page = 1
        self.query_params = query_params
        self.per_page = per_page
        self.all_count = all_count
        self.pager_page_count = pager_page_count
        pager_count, b = divmod(all_count, per_page)
        if b != 0:
            pager_count += 1
        self.pager_count = pager_count

        half_pager_page_count = int(pager_page_count / 2)
        self.half_pager_page_count = half_pager_page_count

    @property
    def start(self):
        """
        数据获取值起始索引
        :return:
        """
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        """
        数据获取值结束索引
        :return:
        """
        return self.current_page * self.per_page

    def page_html(self):
        """
        生成HTML页码
        :return: 生成的HTML页码字符串
        """
        # 如果数据总页码小于11页
        if self.pager_count < self.pager_page_count:
            pager_start = 1
            pager_end = self.pager_count
        else:
            # 数据页码已经超过11页
            # 判断当前页是否小于等于5页
            if self.current_page <= self.half_pager_page_count:
                pager_start = 1
                pager_end = self.pager_page_count
            else:
                # 当前页加上5大于总页码
                if (self.current_page + self.half_pager_page_count) > self.pager_count:
                    pager_end = self.pager_count
                    pager_start = self.pager_count - self.pager_page_count + 1
                else:
                    pager_start = self.current_page - self.half_pager_page_count
                    pager_end = self.current_page + self.half_pager_page_count

        page_list = []

        # 判断当前页是否为第1页
        if self.current_page <= 1:
            prev = '<li class="page-item disabled"><a class="page-link" href="#">上一页</a></li>'
        else:
            # 当前页的前一页
            self.query_params['page'] = self.current_page - 1
            prev = '<li class="page-item"><a class="page-link" href="%s?%s">上一页</a></li>' % (
                self.base_url, self.query_params.urlencode())
        page_list.append(prev)

        # 生成页码列表
        for i in range(pager_start, pager_end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                tpl = '<li class="page-item active"><a class="page-link" href="%s?%s">%s</a></li>' % (
                    self.base_url, self.query_params.urlencode(), i,)
            else:
                tpl = '<li class="page-item"><a class="page-link" href="%s?%s">%s</a></li>' % (
                    self.base_url, self.query_params.urlencode(), i,)
            page_list.append(tpl)

        # 判断当前页是否为最后一页
        if self.current_page >= self.pager_count:
            nex = '<li class="page-item disabled"><a class="page-link" href="#">下一页</a></li>'
        else:
            # 当前页的下一页
            self.query_params['page'] = self.current_page + 1
            nex = '<li class="page-item"><a class="page-link" href="%s?%s">下一页</a></li>' % (
                self.base_url, self.query_params.urlencode(),)
        page_list.append(nex)

        # 拼接HTML页码字符串
        page_str = "".join(page_list)
        return page_str
