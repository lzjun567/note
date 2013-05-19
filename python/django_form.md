Django----Form的来龙去脉（-）使用篇
-------------------------------
*（注：纯属个人学习总结，不一定适合你）*  

Django 的Form表单的功能包括：  
1. 自动生成HTML表单元素  
2. 检查表单数据的合法性  
3. 如果验证错误，重新显示表单（数据不会重置）  
4. 数据类型转换  

与表单相关的对象包括：  
**Widget**：用来渲染成HTML元素的工具，如：forms.Textarea对应HTML中的`<textarea>`标签  
**Field**：代表一个Form对象中的一个字段，如：EmailField表示email字段，如果这个字段不是有效的email格式，就会产生错误。  
**Form**：Form就是一系列Field的集合，负责验证和显示HTML元素
**Form Media**：用来渲染表单的CSS和JavaScript资源。  

####Form Objects
Form对象封装了一系列Field和验证规则，Form类都必须继承制*django.forms.Form*，定义Form有两种方式:  

方法一：直接继承From   

    from django import forms
    class ContactForm(forms.Form):
        subject = forms.CharField(max_length=100,label='主题')
        message = form.CharField(widget=forms.TextArea)
        sender = form.EmailField()
        cc_myself = forms.BooleanField(required=False)

方法二：结合Model，继承django.forms.ModelForm  

    #models.py
    class Contact(models.Model):
        title = models.CharField(max_length=30)
        content = models.CharField(max_length=20)
    
    #form.py
    class ConotactForm(ModelForm):
        class Meta:
        model = Contact
        field = ('title','content')  #只显示model中指定的字段

####在视图（view）中使用form 
在view函数中使用form的一般模式如下：  

    form django.shortcuts import render
    form django.http import HttpResponseRedirect
    
    def contact(request):
        if request.method=="POST":
            form = ContactForm(request.POST)
            if form.is_valid():  #所有验证都通过
                #do something处理业务
                return HttpResponseRedirect('/')
        else:
            form = ContactForm()
        return render(request,'contact.html',{'form':form})

contact.html:  

    <form action='/contact/' method='POST'>
        {% for field in form %}
            <div class = 'fieldWrapper'>
                {{field.label_tag}}:{{field}}
                {{field.errors}}
            </div>
        {% endfor %}
        <div class='fieldWrapper'> <p><input type='submit' value='留言'></p></div>
    </form>

####处理表单数据  

form.is_valid()返回true后，表单数据都被存储在form.cleaned_data对象中（字典对象），而且数据会被自动转换为Python对象，如：在form中定义了DateTimeField，那么该字段将被转换为datetime类型，还有诸如：IntegerField、FloatField  

    if form.is_valid():
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        sender = form.cleaned_data['sender']
        cc_myself = form.cleaned_data['cc_myself']
    
        recipients = ['info@example.com']
        if cc_myself:
            recipients.append(sender)
    
        from django.core.mail import send_mail
        send_mail(subject, message, sender, recipients)
        return HttpResponseRedirect('/thanks/') # Redirect after POST


####在模版中显示表单：
显示form找template中的方法多种多样，也可以自定义：  

    <form action="/contact/" method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit" />
    </form>

还是使用form.as_table、form.as_ul，如果要自定义，你只要获取到每个元素的值就行：  

    <form action="/contact/" method="post">
        {{ form.non_field_errors }}
        <div class="fieldWrapper">
            {{ form.subject.errors }}
            <label for="id_subject">Email subject:</label>
            {{ form.subject }}
        </div>
        <div class="fieldWrapper">
            {{ form.message.errors }}
            <label for="id_message">Your message:</label>
            {{ form.message }}
        </div>
        <div class="fieldWrapper">
            {{ form.sender.errors }}
            <label for="id_sender">Your email address:</label>
            {{ form.sender }}
        </div>
        <div class="fieldWrapper">
            {{ form.cc_myself.errors }}
            <label for="id_cc_myself">CC yourself?</label>
            {{ form.cc_myself }}
        </div>
        <p><input type="submit" value="Send message" /></p>
    </form>
每个form字段都可以使用 {{form.name_of_field}}得到。

也可以通过迭代form，每个迭代元素对应的是form里面的field  

    <form action="/contact/" method="post">
        {% for field in form %}
            <div class="fieldWrapper">
                {{ field.errors }}
                {{ field.label_tag }}: {{ field }}
            </div>
        {% endfor %}
        <p><input type="submit" value="Send message" /></p>
    </form>
{{field}}有如下属性：  

{{field.lable}}，如：*Email address*  
{{field.label\_tag}}，如： `<label for=id_email>Email address</label>`  
{{field.value}} 如：someone.@gmail.com  
{{field.error}}  

参考：https://docs.djangoproject.com/en/dev/topics/forms/  
