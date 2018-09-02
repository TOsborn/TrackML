"""
TrackML feature building by event[s]

    - Create spark session and pass in as first element to function.
    EX: spark = SparkSession.builder.appName("abs_tz").getOrCreate()

    - Pass in list of events to return
    EX: events_list = ['000001000','000001001','000001002']    

    - Function call
    from merge_events import merge_event_dataframes
    event_df = merge_event_dataframes(spark, events_list)
"""

__authors__ = ['Matt Strautmann']

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from pyspark.sql.functions import col
from pyspark.sql.functions import abs, sqrt, udf
from pyspark.ml.regression import LinearRegression

    
def merge_event_dataframes(spark, events_list):
    """Merge multiple event features into a single dataframe for use in Kalman filter.

    Handles blacklisted particles by left joining to the previously filtered particles-in-order.

    Parameters
    ----------
        spark : SparkSession.
        
        events_list : Python array of events list.

    Returns
    -------
        pyspark.sql.DataFrame : `particles-in-order` augmented with additional columns: 
                                    tx,ty,tz,tpx,tpy,tpz,
                                    weight,x,y,z,pt,nhits,
                                    total_value,event_id
    """

    # Source path urls
    in_order_url   = '/home/ec2-user/SageMaker/efs/particles-in-order/event'
    train_url      = '/home/ec2-user/SageMaker/efs/dataset/train/event'
    
    for idx,fn in enumerate(events_list):
        print('Working on event, ', fn)
        df     = spark.read.csv(in_order_url + fn + '-hit_orders.csv',header=True,inferSchema=True)
        df1    = spark.read.csv(train_url + fn + '-truth.csv',header=True,inferSchema=True)
        df2    = spark.read.csv(train_url + fn + '-hits.csv',header=True,inferSchema=True)
        cells  = spark.read.csv(train_url + fn + '-cells.csv', header=True,inferSchema=True)

        # tx, ty, tz, tpx, tpy, tpz
        dfjoin = df.alias('a').join(df1.alias('b'), df.hit_id == df1.hit_id, "left_outer")\
                 .select([col('a.'+ x) for x in df.columns] + [df1.tx,df1.ty,df1.tz,df1.tpx,df1.tpy,df1.tpz,df1.weight])
        # Add x,y,z
        dfjoin = dfjoin.alias('a').join(df2.alias('b'), dfjoin.hit_id == df2.hit_id).select([col('a.'+ x) for x in dfjoin.columns] + [df2.x,df2.y,df2.z])

        # pt (transverse momentum)
        pt = dfjoin.withColumn('pt', sqrt(dfjoin['tpx']**2+ dfjoin['tpy']**2))
        
        # count number of cells a particle passes through for a particular hit.
        cell_count = cells.groupBy('hit_id').agg({'hit_id':'count'})
        nhits  = pt.alias('a').join(cell_count.alias('b'), pt.hit_id == cell_count.hit_id)\
                .select([col('a.'+ x) for x in pt.columns] + [col('b.count(hit_id)').alias("nhits")])

        # total value
        values = cells.groupBy('hit_id').agg({'value':'sum'})
        total_value = nhits.alias('a').join(values.alias('b'), nhits.hit_id == values.hit_id)\
                      .select([col('a.'+ x) for x in nhits.columns] + [col('b.sum(value)').alias("total_value")])\
                      .orderBy(['particle_id','hit_id','hit_order'])
        
        if idx == 0:
            event_df = total_value.withColumn('event_id', lit(fn))
        else:
            temp_event_df = total_value.withColumn('event_id', lit(fn))
            event_df = event_df.union(temp_event_df)
        
    return event_df