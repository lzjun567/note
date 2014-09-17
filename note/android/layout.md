####ListActivity

####ListView
显示ListView时，相关的东西有：  
1. listview（用来显示数据的列表），ListView的每一项都是TextView。  
2. Data（显示的数据）
3. 适配器ListAdapter（用来绑定Data和ListView） 
#####ListAdapter
ListAdapter是个接口，直接子类有：ArrayAdapter<T>、SimpleAdapter、CursorAdapter。

#####SimpleAdapter

    SimpleAdapter (Context context, List<? extends Map<String, ?>> data, int resource, String[] from, int[] to)
resource:  布局layout，可以自定义，android自带的布局有：  

    1. Android.R.layout.simple_list_item_1：每一项只有一个TextView
    2. Android.R.layout.simple_list_item_2：每一项有两个TextView
    3. Android.R.layout.simpte.list_item_single_choice,每一项有一个TextView，但是这一项可以被选中。
    
from(名字数组)、to(TextView数组)：把map中的那一列放到哪个TextView中去 
