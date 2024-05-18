// ================= Saul ==================

#include <glib.h>
#include "nvdsmeta_schema.h"

typedef struct NvDsEventMsgMeta {
  /** Holds the event's type. */
  NvDsEventType type;
  /** Holds the object's type. */
  NvDsObjectType objType;
  /** Holds the object's bounding box. */
  NvDsRect bbox;
  /** Holds the object's geolocation. */
  NvDsGeoLocation location;
  /** Holds the object's coordinates. */
  NvDsCoordinate coordinate;
  /** Holds the object's signature. */
  NvDsObjectSignature objSignature;
  /** Holds the object's class ID. */
  gint objClassId;
  /** Holds the ID of the sensor that generated the event. */
  gint sensorId;
  /** Holds the ID of the analytics module that generated the event. */
  gint moduleId;
  /** Holds the ID of the place related to the object. */
  gint placeId;
  /** Holds the ID of the component (plugin) that generated this event. */
  gint componentId;
  /** Holds the video frame ID of this event. */
  gint frameId;
  /** Holds the confidence level of the inference. */
  gdouble confidence;
  /** Holds the object's tracking ID. */
  gint trackingId;
  /** Holds a pointer to the generated event's timestamp. */
  gchar *ts;
  /** Holds a pointer to the detected or inferred object's ID. */
  gchar *objectId;

  /** Holds a pointer to a string containing the sensor's identity. */
  gchar *sensorStr;
  /** Holds a pointer to a string containing other attributes associated with
   the object. */
  gchar *otherAttrs;
  /** Holds a pointer to the name of the video file. */
  gchar *videoPath;
  /** Holds a pointer to event message meta data. This can be used to hold
   data that can't be accommodated in the existing fields, or an associated
   object (representing a vehicle, person, face, etc.). */
  gpointer extMsg;
  /** Holds the number of line-crossings captured in the current frame */
  gint lcNum;
  /** Holds the stream ID */
  gint streamId;
  /** Holds the size of the custom object at @a extMsg. */
  guint extMsgSize;
  
  //---------------------- CUSTOM CODE --------------------//
  // Conteo Saul
  gchar names[50][10]; // 0:[in1, out1, in2, out2], 1:[in1,out1] 
  gint counts[50];   
  //-----------------------------------------------------------------------------------------//
  //
} NvDsEventMsgMeta;

typedef struct _NvDsEvent {
  /** Holds the type of event. */
  NvDsEventType eventType;
  /** Holds a pointer to event metadata. */
  NvDsEventMsgMeta *metadata;
} NvDsEvent;
