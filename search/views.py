from django.shortcuts import render

from .document import PropertyDocument, UserDocument

from property.models import Property

# Create your views here.




def property_search(request):
    query = request.GET.get('q', '')
    properties = set()
    if query:
        # Property Queries
        p = PropertyDocument.search().query("multi_match", query=query, fields=[
            'title',
            'address',
            'description',
            'city',
            'state',
            'zip_code',
            'country',
            'features.name',  # Include nested field in multi_match
            'property_type.name',  # Assuming 'property_type' is also nested
        ], fuzziness='auto')
        fuzzy_properties = p.to_queryset()

        gen = PropertyDocument.search().query("multi_match", query=query)
        general_properties = gen.to_queryset()

        f = PropertyDocument.search().query('nested', path='features', query={'match': {'features.name': query}})
        feature_properties = f.to_queryset()

        pt = PropertyDocument.search().query("nested", path='property_type', query={'match': {'property_type.name': query}})
        properties_type = pt.to_queryset()

        # Combine the results (remove duplicates)
        properties = set(list(fuzzy_properties) + list(general_properties) + list(feature_properties) + list(properties_type))

        # User Queries
        u = UserDocument.search().query("multi_match", query=query, fields=[
            'username',
            'first_name',
            'last_name',
            'gender',
             # Include nested fields in multi_match
            'managers.company_name',
            'managers.properties_managed',
            'managers.about',
        ], fuzziness='auto')
        users = u.to_queryset()

        
    else:
        properties = Property.objects.all()

    context = {
        'users': users, 
        'properties': properties,
        'query': query}
    return render(request, 'search/search_results.html', context)

