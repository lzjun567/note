Android RecyclerView CardView指南
==================
Android L最新支持包推出两个UI控件**RecycleView**和**CardView**。RecyclerView是更先进，更灵活的ListView，这是一个很大的进步，因为ListView是UI组件中最常用的控件之一。此外，CardView控件是一个全新的组件。在这篇教程中将解释如何使用这两个控件以及如何混合使用它们，首先来来深入了解一下RecyclerView。  
####RecyclerView
正如前面说RecyclerView是更加灵活的ListView，尽管它引进了一些复杂的东西。我们都知道如何在app中使用ListView，并且如果想要提高ListView的性能，那么可以使用一种叫**ViewHolder**的模式。这个模式由一个简单类组成，它持有ListView中每一行所包含的UI组件的引用。这种模式避免列表显示的时候总是查找那些UI组件。尽管该模式引进了这点好处但我们仍可以不使用这种模式来实现ListView。而RecyclerView强制我们使用ViewHolder模式来提高系统的性能。为了说明如何使用RecyclerView，我们可以创建一个简单的app来显示通讯录卡片列表。第一件事就是创建主布局文件，RecyclerView很像ListView，我们可以用相同的方式来使用它们。  
    
    <RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
      xmlns:tools="http://schemas.android.com/tools"
      android:layout_width="match_parent"
      android:layout_height="match_parent"
      android:paddingLeft="@dimen/activity_horizontal_margin"
      android:paddingRight="@dimen/activity_horizontal_margin"
      android:paddingTop="@dimen/activity_vertical_margin"
      android:paddingBottom="@dimen/activity_vertical_margin"
      tools:context=".MyActivity">
      <android.support.v7.widget.RecyclerView
             android:id="@+id/cardList"
             android:layout_width="match_parent"
             android:layout_height="match_parent"
       />    
    </RelativeLayout>
你应该注意到上面的layout了，RecycleView位于Android支持库中，所以我们要修改*bulid.gradle*文件来包含该依赖。  
    
    dependencies {
       ...    
       compile 'com.android.support:recyclerview-v7:21.0.0-rc1'
    }
现在就可以在`onCreate`方法中我们来获取RecycleView的引用并且配置它。  
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
          super.onCreate(savedInstanceState);
          setContentView(R.layout.activity_my);
          RecyclerView recList = (RecyclerView) findViewById(R.id.cardList);
          recList.setHasFixedSize(true);
          LinearLayoutManager llm = new LinearLayoutManager(this);
          llm.setOrientation(LinearLayoutManager.VERTICAL);
          recList.setLayoutManager(llm);
    }

你会注意到ReclerView与ListView的区别，RecycleView需要一个*布局管理器*，这个组件把列表项视图放到了行里面，来决定什么时候去循环视图。这个库提供了一个默认的布局管理器叫做`LinearLayoutManager`。  

####CardView
CardView UI组件在卡片里面显示更多信息。可以自定义它的圆角、阴影等效果。现在用这个组件来展示通讯信息。卡片将作为RecyclerView的行，稍后我们能看到如何集成这两个组件，现在来定义该卡片的布局。  
    
    <android.support.v7.widget.CardView
      xmlns:card_view="http://schemas.android.com/apk/res-auto"
      xmlns:android="http://schemas.android.com/apk/res/android"
      android:id="@+id/card_view"
      android:layout_width="match_parent"
      android:layout_height="match_parent"
      card_view:cardCornerRadius="4dp"
      android:layout_margin="5dp">

    <RelativeLayout
      android:layout_width="match_parent"
      android:layout_height="match_parent">

     <TextView
         android:id="@+id/title"
         android:layout_width="match_parent"
         android:layout_height="20dp"
         android:background="@color/bkg_card"
         android:text="contact det"
         android:gravity="center_vertical"
         android:textColor="@android:color/white"
         android:textSize="14dp"/>

    <TextView
        android:id="@+id/txtName"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Name"
        android:gravity="center_vertical"
        android:textSize="10dp"
        android:layout_below="@id/title"
        android:layout_marginTop="10dp"
        android:layout_marginLeft="5dp"/>

    <TextView
        android:id="@+id/txtSurname"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Surname"
        android:gravity="center_vertical"
        android:textSize="10dp"
        android:layout_below="@id/txtName"
        android:layout_marginTop="10dp"
        android:layout_marginLeft="5dp"/>

    <TextView
        android:id="@+id/txtEmail"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Email"
        android:textSize="10dp"
        android:layout_marginTop="10dp"
        android:layout_alignParentRight="true"
        android:layout_marginRight="150dp"
        android:layout_alignBaseline="@id/txtName"/>

    </RelativeLayout>

正如你所看到的，CardView使用非常简单，这个组件在另外一个支持库中，现在来添加依赖：  
    
    dependencies {
        compile 'com.android.support:cardview-v7:21.0.0-rc1'
        compile 'com.android.support:recyclerview-v7:21.0.0-rc1'
    }

####RecyclerView: Adapter
适配器组件提供数据信息，UI组件渲染这些信息，换而言之，一个适配器告诉UI显示哪些信息。因此如果我们想显示通讯信息，我们需要给RecyclerView一个适配器。该适配器必须继承`RecyclerView.Adapter`。传递MyHolder类实现ViewHolder模式。  
    
    public class MyAdapter extends RecyclerView.Adapter<MyHolder> { ..... }

现在我们需要覆盖两个方法以至于能实现我们的逻辑。`onCreateViewHolder`会在新的ViewHolder实例创建的时候被调用，`onBindViewHolder`在SO试图绑定数据的时候调用，换句话说，数据显示在UI中时调用。  

在这个案例中，适配器帮我们把RecyclerView和CardView结合，之前我们定义的卡片布局将作为RecyclerView的通讯录列表的行。在做这个之前，我们需要定义好数据模型（例如：哪些信息需要显示），为了达到这个目的，我们可以定义一个简单类：  
    
    public class ContactInfo {
      protected String name;
      protected String surname;
      protected String email;
      protected static final String NAME_PREFIX = "Name_";
      protected static final String SURNAME_PREFIX = "Surname_";
      protected static final String EMAIL_PREFIX = "email_";
    }
最后，准备创建适配器，如果你还记得之前说过的ViewHolder模式的话，我们需要编写代码来实现它。  
    
    public static class ContactViewHolder extends RecyclerView.ViewHolder {
     protected TextView vName;
     protected TextView vSurname;
     protected TextView vEmail;
     protected TextView vTitle;

     public ContactViewHolder(View v) {
          super(v);
          vName =  (TextView) v.findViewById(R.id.txtName);
          vSurname = (TextView)  v.findViewById(R.id.txtSurname);
          vEmail = (TextView)  v.findViewById(R.id.txtEmail);
          vTitle = (TextView) v.findViewById(R.id.title);
      }
    }
从代码中看出，在类的构造方法中，我们获取到了定义在卡片布局的试图的引用，现在编写适配器代码：  
    
    public class ContactAdapter extends RecyclerView.Adapter<ContactAdapter.ContactViewHolder> {

        private List<ContactInfo> contactList;
    
        public ContactAdapter(List<ContactInfo> contactList) {
                this.contactList = contactList;
        }
    
        @Override
        public int getItemCount() {
              return contactList.size();
        }
    
        @Override
        public void onBindViewHolder(ContactViewHolder contactViewHolder, int i) {
            ContactInfo ci = contactList.get(i);
            contactViewHolder.vName.setText(ci.name);
            contactViewHolder.vSurname.setText(ci.surname);
            contactViewHolder.vEmail.setText(ci.email);
            contactViewHolder.vTitle.setText(ci.name + " " + ci.surname);
       }
    
       @Override
       public ContactViewHolder onCreateViewHolder(ViewGroup viewGroup, int i) {
            View itemView = LayoutInflater.
                        from(viewGroup.getContext()).
                        inflate(R.layout.card_layout, viewGroup, false);
    
            return new ContactViewHolder(itemView);
       }

      public static class ContactViewHolder extends RecyclerView.ViewHolder {
          ...
      }
    }

在代码实现中，绑定数据给试图的时候我们覆盖了`onBindViewHolder`。注意我们再没有去查找UI组件只是简单地引用存储在CcontactViewHolder中的信息。在onCreateViewHolder返回了ContactViewHolder填充布局的行（这个例子中的CardView）。  

运行app，你会看到如下结果：  
    
![android](http://www.binpress.com/images/uploads/38968/android_recyclerview_cardview.png)

完整代码可以在[github](https://github.com/survivingwithandroid/Surviving-with-android/tree/master/Android_RecyclerView_CardView)中查看  

原文：[A Guide to Android RecyclerView and CardView](http://www.binpress.com/tutorial/android-l-recyclerview-and-cardview-tutorial/156)
