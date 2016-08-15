/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// scalastyle:off println
package org.apache.spark.examples.streaming

import kafka.serializer.StringDecoder

import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf

import java.io._

//Importing libraries for Stream analytics
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.regression.StreamingLinearRegressionWithSGD

import scala.util.parsing.json._

/**
 * Consumes messages from one or more topics in Kafka and does wordcount.
 * Usage: ML_GoogleNest_ApcheSpark <brokers> <topics>
 *   <brokers> is a list of one or more Kafka brokers
 *   <topics> is a list of one or more kafka topics to consume from
 *
 * Example:
 *    $ bin/run-example streaming.ML_GoogleNest_ApcheSpark broker1-host:port,broker2-host:port \
 *    topic1,topic2
 */
object ML_GoogleNest_ApcheSpark {


  def main(args: Array[String]) {
    if (args.length < 2) {
      System.err.println(s"""
        |Usage: DirectKafkaWordCount <brokers> <topics>
        |  <brokers> is a list of one or more Kafka brokers
        |  <topics> is a list of one or more kafka topics to consume from
        |
        """.stripMargin)
      System.exit(1)
    }

    StreamingExamples.setStreamingLogLevels()

    val Array(brokers, topics) = args

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("DirectKafkaWordCount")
    val ssc = new StreamingContext(sparkConf, Seconds(2))
	
	
	//Used for taking input from file
	//val trainingData = ssc.textFileStream("/home/ubuntu/training_data").map(LabeledPoint.parse).cache()
	//val testData = ssc.textFileStream("/home/ubuntu/testing_data").map(LabeledPoint.parse)
	
	
	val topicsSet = topics.split(",").toSet
	//println("Topic Set : " + topicsSet)
	val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
	//println( "Keys in kafkaParams : " + kafkaParams.keys )
	//println( "Values in kafkaParams : " + kafkaParams.values  )
	val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topicsSet)

	
	val input_lines = messages.map(_._2)

	val trainingData = input_lines.map { line =>
    val individual_val = line.split(',')
	
	val time_temp1 = individual_val(0).split(":")
	//val time_temp2 = time_temp1(1).split("\"")
	val time = time_temp1(1)
	println("time")
	println(time)
	
	val temperature1 = individual_val(1).split(":")
	val temperature2 = temperature1(1).split("}")
	val temperature = temperature2(0)
	println("values")
	println(temperature)
    LabeledPoint(temperature.toDouble, Vectors.dense(Array(time) map(_.toDouble)))
    }.cache()
	
	
	
	val testData = input_lines.map { line =>
    val individual_val = line.split(',')
	
	val time_temp1 = individual_val(0).split(":")
	//val time_temp2 = time_temp1(1).split("\"")
	val time = time_temp1(1)
	//println("time")
	println(time)
	
	val temperature1 = individual_val(1).split(":")
	val temperature2 = temperature1(1).split("}")
	val temperature = temperature2(0)
	//println("values")
	println(temperature)
    LabeledPoint(temperature.toDouble, Vectors.dense(Array(time) map(_.toDouble)))
    }

	

	
	val numFeatures = 1
	val model = new StreamingLinearRegressionWithSGD().setInitialWeights(Vectors.zeros(numFeatures)).setNumIterations(500).setStepSize(0.00001)
	
	model.trainOn(trainingData)
	model.predictOnValues(testData.map(lp => (lp.label, lp.features))).print()


	/*
    // Create direct kafka stream with brokers and topics
    val topicsSet = topics.split(",").toSet
    val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
    val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](
      ssc, kafkaParams, topicsSet)

    // Get the lines, split them into words, count the words and print
    val lines = messages.map(_._2)
    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map(x => (x, 1L)).reduceByKey(_ + _)
    wordCounts.print()
	*/

    // Start the computation
    ssc.start()
    ssc.awaitTermination()
  }
}
// scalastyle:on println
