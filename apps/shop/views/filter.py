# FILTER PRODUCTS
attrs = {'product' : ['brand'], 'variant' : ['color', 'sizes'],}
QueryParams = Q()
for key, value in attrs.items():
    add = ''
    if key == 'product':
        add = 'parent__'
    for attr in value:
        params = kwargs[attr]
        if params != None:
            params = params.split(',')
            QueryParams &= Q(**{add + attr + '__slug__in':params})

self.context['variants'] = self.context['variants'].filter(QueryParams)
self.context['products'] = self.context['products'].filter(variant__in=self.context['variants']).distinct()
filters = self.selected_product_filters(kwargs['filters'])

filterGroups = ['brand','color','sizes']

def FilterQuery(excluded):
    QueryParams = {}
    curGroup = []
    for group in filterGroups:
        if group in filterGroups and group in self.context.keys() and group != excluded: 
            curGroup.append(group)
    for group in curGroup:
        params = self.kwargs[group]
        try:
            Variant._meta.get_field(group)
            parent = ''
        except:
            parent = 'parent__'
        if params != None:
            QueryParams = {parent + group + '__slug__in' : params.split(',')}
    

    for item in self.context[excluded]:
        ItemQueryParams = copy.deepcopy(QueryParams)   
        ItemQueryParams['pk__in'] = item.json_variant_pks
        variants = self.category_variants.filter(**ItemQueryParams)
        item.len = len(variants)
        params = self.kwargs[excluded]
        if params != None:
            if item.slug in params:
                item.checked = True
    return curGroup

for group in filterGroups:
    FilterQuery(group)