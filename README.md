django-simple-formwizard
========================

**django-simple-formwizard** is a simple session based form wizard for django applications.

Quickstart:
========================

Install django-tinymce-filebrowser:

    $ pip install django-tinymce-filebrowser


In views:
---------

Define steps configuration:

    MY_WIZARD_STEPS = [
        {'name': 'Step Mane', 
         'url_name': 'url-to-step',
         'url_params': [list of url params],
         'anonymous_required': False},
        ...
    ]
    
Create wizard object

    wizard = Wizard(request, MY_WIZARD_STEPS)

Forms initial data:
    
    my_form = MyForm(initial=wizard.data.get('my_data', {}))

Setting data:
    
    wizard.set_data({'my_data': my_form})

Example:

    my_form = MyForm(initial=wizard.data.get('my_data', {}))

    if request.method == 'POST':
        my_form = MyForm(request.POST)
        
        if my_form.is_valid():
            wizard.set_data({'my_data': my_form})
            return redirect_to_next_step
        

Step url and redirects:

    wizard.steps[step_index]['url']


Access and use data:
    
    Access POST data:
    wizard.data['post']
    
    Access user data:
    wizard.data['my_data_key']


Helper decorators:

Check current wizard session identificator

    @wizard_check_id(redirect_to='url_name')


Check user key

    @wizard_check_data([list of keys], redirect_to='url_name')


In templates:
-------------

    {% for step in wizard.steps %}
        {% if step.passed %}
            <a href="{{ step.url }}"{% if step.is_current %} class="active"{% endif %}>
                {{ step.name }}
            </a>
        {% else %}
            <li{% if step.is_current %} class="active"{% endif %}>{{ step.name }}</li>
        {% endif %}
    {% endfor %}

Step properties:

- passed - indicate that this step is passed
- is_current - indicate that this step is active
- name - step name
- url - url of the step
- index - step index
    
Access prev steps:

    {{ wizard.current_step.prev }}

API:
-----

Wizard object public methods and properties:

Properties:

- request - request object
- data - saved user data
- user - user instance
- current_step - the current step
- steps - all availible steps
- id - wizard unique identificator

Methods:

    - set_data({'data_key': form}) - set form data with specified key
    - cleanup() - cleanup the session

Example:
---------

views.py

    WIZARD_STEPS = [
        {'name': 'Step 1', 'url_name': 'wizard-step1'},
        {'name': 'Step 2', 'url_name': 'wizard-step2'},
        {'name': 'Preview','url_name': 'wizard-preview'}
    ]


    def step1(request):
        wizard = Wizard(request, WIZARD_STEPS)
        my_form = MyForm(initial=wizard.data.get('step1_data', {}))

        if request.method == 'POST':
            my_form = MyForm(request.POST)
            
            if my_form.is_valid():
                wizard.set_data({'step1_data': my_form})
                return redirect(wizard.steps[1]['url'])
        
        return render(request, 'step.html', {'wizard': wizard, 'my_form': my_form})
        

    @wizard_check_id(redirect_to='wizard-step1')
    @wizard_check_data(['step1_data'], redirect_to='wizard-step1')
    def step2(request):
        wizard = Wizard(request, WIZARD_STEPS)
        form1 = MyForm1(initial=wizard.data.get('step2_data1', {}))
        form2 = MyForm2(initial=wizard.data.get('step2_data2', {}))

        if request.method == 'POST':
            form1 = MyForm1(request.POST)
            form2 = MyForm2(request.POST)
            
            if form1.is_valid() and form2.is_valid():
                wizard.set_data({'step2_data1': form1})
                wizard.set_data({'step2_data2': form2})
                
                return redirect(wizard.steps[2]['url'])
        
        return render(request, 'step.html', {'wizard': wizard, 'form1': form1, 'form2': form2})
        

    @wizard_check_id(redirect_to='wizard-step1')
    @wizard_check_data(['step2_data1', 'step2_data2'], redirect_to='wizard-step1')    
    def preview(request):
        wizard = Wizard(request, WIZARD_STEPS)
        data = {
            'step1_data': wizard.data['step1_data'],
            'step2_data1': wizard.data['step2_data1'],
            'step2_data2': wizard.data['step2_data2'],
        }
        
        if 'confirm' in request.GET:
            my_form = MyForm(wizard.data['post'])
            form1 = MyForm1(wizard.data['post'])
            form2 = MyForm2(wizard.data['post'])
            
            if my_form.is_valid() and form1.is_valid() and form2.is_valid():
                my_form.save()
                form1.save()
                form2.save()
                wizard.cleanup()
                
                return redirect('wizard-done')
        
        return render(request, 'preview.html', {'wizard': wizard, 'data': data})

step.html

    <ul class="wizard-tabs">
        {% for step in wizard.steps %}
            {% if step.passed %}
                <a href="{{ step.url }}"{% if step.is_current %} class="active"{% endif %}>{{ step.name }}</a>
            {% else %}
                <li{% if step.is_current %} class="active"{% endif %}>{{ step.name }}</li>
            {% endif %}
        {% endfor %}
    </ul>

    <form action="./" method="post">
        {% csrf_token %}
        {{ my_form }}
        <div>
            {% if wizard.current_step.index > 0 %}
                <a href="{{ wizard.current_step.prev }}">&laquo; Back</a>
            {% endif %}
            <button type="submit">Next &raquo;</button>
        </div>
    </form>
