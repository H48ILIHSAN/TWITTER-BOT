var CronJob = require('cron').CronJob;
var twit = require('twit');
var AziziConfig = require('../app/AziziConfig.js');
var AziziQuery = require('../app/AziziQuery.json');
var AziziTwitter = new twit(AziziConfig);
var AziziTwit = Object.keys(AziziQuery.tweetData.scheduledTweet).length;
var Azizi = AziziQuery.tweetData
var FloraConfig = require('../app/FloraConfig.js');
var FloraQuery = require('../app/FloraQuery.json');
var FloraTwitter = new twit(FloraConfig);
var FloraTwit = Object.keys(FloraQuery.tweetData.scheduledTweet).length;
var Flora = FloraQuery.tweetData

//Scheduled tweet
new CronJob('* * * * *', function () {
    let failedTweet = []

    const newDate = new Date()
    const hour = newDate.getHours('en-US', { timezone: 'Asia/Jakarta' })
    const minute = newDate.getMinutes('en-US', { timezone: 'Asia/Jakarta' })
    const time = `${hour}:${minute}`
    console.log('START AT ' + time)
  
    for (let i = 0; i < AziziTwit; i++) {
      if (Azizi.scheduledTweet[i].time == time) {
        AziziTwitter.post('statuses/update', {
            status: Azizi.scheduledTweet[i].message
        }, function (err, data, response) {
          if (err) {
            console.error('ERROR: ' + err.message)
            console.log(Azizi.scheduledTweet[i])
            failedTweet.push(Azizi.scheduledTweet[i])
          } else {
            console.log('SUCCESS!\n' + Azizi.scheduledTweet[i].message)
          }
        })
      }
    }

    for (let i = 0; i < FloraTwit; i++) {
        if (Flora.scheduledTweet[i].time == time) {
          FloraTwitter.post('statuses/update', {
              status: Flora.scheduledTweet[i].message
          }, function (err, data, response) {
            if (err) {
              console.error('ERROR: ' + err.message)
              console.log(Flora.scheduledTweet[i])
              failedTweet.push(Flora.scheduledTweet[i])
            } else {
              console.log('SUCCESS: ' + Flora.scheduledTweet[i].message)
            }
          })
        }
      }

  }, null, true, 'Asia/Jakarta').start()
  
  // Failed Tweet
  new CronJob('*/5 * * * * *', function () {

    if (AziziQuery.tweetData.failedTweet) {
      let failedTweet = AziziQuery.tweetData.failedTweet
      console.log('FAILED!')
      for (let i = 0; i < AziziQuery.tweetData.failedTweet; i++) {
        AziziTwitter.post('statuses/update', {
            status: AziziQuery.tweetData.failedTweet[i].message
        }, function (err, data, response) {
          if (err) {
            console.error('ERROR: ' + err.message)
          } else {
            console.log('SUCCESS: ' + AziziQuery.tweetData.failedTweet[i].message)
            failedTweet.splice(i, 1)
          }
        })
      }
    } else {
        console.log('RUNING!')
      }

    if (FloraQuery.tweetData.failedTweet) {
      let failedTweet = FloraQuery.tweetData.failedTweet
      console.log('FAILED!')
      for (let i = 0; i < FloraQuery.tweetData.failedTweet; i++) {
        FloraTwitter.post('statuses/update', {
            status: FloraQuery.tweetData.failedTweet[i].message
        }, function (err, data, response) {
          if (err) {
            console.error('ERROR: ' + err.message)
          } else {
            console.log('SUCCESS!\n' + FloraQuery.tweetData.failedTweet[i].message)
            failedTweet.splice(i, 1)
          }
        })
      }
      
    } else {
      console.log('RUNING!')
    }
  }, null, true, 'Asia/Jakarta').start()
  
